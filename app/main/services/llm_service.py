from main.models.client_bot import ClientBot
from main.models.client import Client
from threading import  Lock
from utils._tokenizers import TokenizerManager
from main.services.bot_service import BotService
from flask import current_app
import requests
import tiktoken
import re
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import openai
import time
class LLMService:
    
    def __init__(self ):
      
        self.locks = {}
        self.tokenizer_manager = TokenizerManager()

        self.bot_service = BotService()
        # self.queues = {}
    
    @property
    def db_session(self):
        from main import db  
        return db.session
    
    def get_token_count(self, text: str) -> int:
        # Get the tokenizer instance
        tokenizer = self.tokenizer_manager.sync_get_tokenizer()
        # Tokenize the input text and get the token IDs
        encoding = tokenizer.encode(text)  # Use encode() to get token information
        
        # Return the number of tokens
        return len(encoding.ids)  # encoding.ids is a list of token IDs
    
    def get_lock(self, clientId):
        # print("get_lock")
        if clientId not in self.locks:
            self.locks[clientId] = Lock()
        return self.locks[clientId]

    def check_client_exists(self, client_id):
        return self.db_session.query(Client).filter_by(id=client_id).first() is not None
    
    # def check_client_exists(self, client_id):
    #     return Client.objects.get(id=client_id) is not None

    def updateTokenUsage(self, client_id, bot_id, tkns_used):
        
        with self.get_lock(client_id):
            client_bot = self.db_session.query(ClientBot).filter_by(client_id=int(client_id), bot_id=int(bot_id)).first()
            if client_bot:
                client_bot.tkns_used += tkns_used
                client_bot.tkns_remaining -= tkns_used
                self.db_session.commit()  
                return True  
        return False  

    # def updateTokenUsage(self, clientId, botId, tkns_used):
    #     # print("updateTokenUsage")
    #     with self.get_lock(clientId):
    #         client = Client.objects.get(id=clientId)
    #         for bot in client.bots:
    #             if bot.id == botId:
    #                 bot.tkns_used += tkns_used
    #                 bot.tkns_remaining -= tkns_used
    #                 client.save()
    def createThread(self, apiToken):
        # print("createThread")
        url = 'https://api.openai.com/v1/threads'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta': 'assistants=v2'
        }

        response = requests.post(url, headers=headers)
        return response.json()['id']

    def sendMessageThread(self, apiToken, threadID, message, clientId):
        # print("sendMessageThread")
        url = f'https://api.openai.com/v1/threads/{threadID}/messages'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta': 'assistants=v2'
        }

        data = [
            {
            "role": "user",
            "content": message
        }
        ]
        num_tokens = self.getTokenCount(data)
        # self.updateTokenUsage(clientId, num_tokens)

        response = requests.post(url, headers=headers, json=data)
        return response.json(), num_tokens

    def runThread(self, apiToken, threadID, assistant_ID):
        # print("runThread")
        url = f'https://api.openai.com/v1/threads/{threadID}/runs'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta': 'assistants=v2'
        }

        data = {"assistant_id": assistant_ID}

        response = requests.post(url, headers=headers, json=data)
        return response.json()['id']

    def checkRunStatus(self, apiToken, threadID, runID):
        # print("checkRunStatus")
        url = f'https://api.openai.com/v1/threads/{threadID}/runs/{runID}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta': 'assistants=v2'
        }
        response = requests.get(url, headers=headers)
        print("checkRunStatus : ", response.json())
        return response.json()['status']

    def retrieveMessage(self, apiToken, threadID, clientId):
        # print("retrieveMessage")
        url = f'https://api.openai.com/v1/threads/{threadID}/messages'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta': 'assistants=v2'
        }
        response = requests.get(url, headers=headers)

        reply_data = response.json()['data'][0]['content'][0]['text']['value']
        reply_tokens = self.getTokenCount([{"role": "assistant", "content": reply_data}])
        # self.updateTokenUsage(clientId, reply_tokens)
        return reply_data, reply_tokens            
    
    def convert_to_valid_session_id(self, session_id):
        # Replace all invalid characters with underscores
        print("running conversion")
        print(session_id)
        if not isinstance(session_id, str):
            session_id = str(session_id)
        valid_session_id = re.sub(r'[^0-9a-zA-Z._:-]', '_', session_id)
        print(valid_session_id)
        return valid_session_id 
                      
    def process_request(self, message, botId, sessionId, threadId):
        try:
            bot = self.bot_service.returnBot(bot_id=botId)
            print("bot", bot)
            # region_name = current_app.config['REGION_NAME']
            # agent_id = bot['agent_id']
            assistant_ID = bot['assistant_id']
            # model_id = current_app.config['MODEL_ID']
            # threadID = self.chat_service.getThreadId(session_id=sessionId)
            # session_id = self.convert_to_valid_session_id(sessionId)

            openai.api_key = current_app.config['OPENAI_API_KEY'],
            client = openai.OpenAI()
            message = client.beta.threads.messages.create(thread_id=threadId, role="user", content=message)
            thread_run = client.beta.threads.runs.create(thread_id=threadId, assistant_id=assistant_ID,instructions="you are a science tutor for stage 3 students.Main lesson topics are:1.Looking After Plants 2.Mixing Materials 3.Light and Shadows 4.Staying Alive 5.Forces & Magnets 6.The Earth & Moon.Stricly stick to these topics and base all your answers on the training data.")
            
            while True:
                try:
                    run = client.beta.threads.runs.retrieve(thread_id=threadId, run_id=thread_run.id)
                    if run.completed_at:
                        elapsed_time = run.completed_at - run.created_at
                        formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                        print(f"Run completed in {formatted_elapsed_time}")
                        messages = client.beta.threads.messages.list(thread_id=threadId)
                        run_steps = client.beta.threads.runs.steps.list(thread_id=threadId, run_id=thread_run.id)
                        last_message = messages.data[0]
                        response = last_message.content[0].text.value
                        return{
                            "message": response,
                            "completion_tokens":run_steps.data[0].usage.completion_tokens,
                            "prompt_tokens":run_steps.data[0].usage.prompt_tokens,
                            "total_tokens":run_steps.data[0].usage.total_tokens,
                            "threadId":run_steps.data[0].thread_id
                        }
                            
                except Exception as e:
                        print((f"An error occurred while retrieving the run: {e}"))
                        break

        except Exception as e:
            print(e)
        
        # print('completion : ',completion)
        # print(type(completion))
        # # output_tkns = llm.get_num_tokens(completion)
        # output_tkns = self.getTokenCount([{"role": "user", "content": completion}])
        # self.updateTokenUsage(clientId, botId, (input_tkns + output_tkns))
        # print("tkn in output : ", output_tkns)
        # self.chat_service.storeMessage(sessionId, message, completion)
        # return {
        #     "message": completion,
        #     "token usage" : input_tkns + output_tkns
        # }

    def connectModel(self, message,clientId,  botId, sessionId, threadId):
        try:    
            remaining_tkns = self.checkRemainingTokens(clientId, botId)
            msg_tkn = self.getTokenCount([{"role": "user", "content": message}])
            if (msg_tkn * 2 >= remaining_tkns) or (remaining_tkns < 1000):
            # if (remaining_tkns < 1000):
                return {"error": "Remaining tokens are too low. Please recharge to get replies"}
            if remaining_tkns <= 0:
                return {"error": "Token limit reached"}

            # Check moderation
            moderation_result = self.moderate_content(
                current_app.config['OPENAI_API_KEY'],
                message
            )
            if moderation_result["flagged"]:
                return {
                    "error": "Message contains content that violates our policy.",
                    "categories": moderation_result["categories"]
                }            
            
            result = self.process_request(message, botId, sessionId, threadId)
            print("tkns ",result["total_tokens"] )
            self.updateTokenUsage( clientId, botId, result["total_tokens"])
            return result
        
        except Exception as e: 
            print('error @ 159', str(e))
            return {"error": str(e)}

    def checkRemainingTokens(self, client_id, bot_id):
        print('running check tkn', client_id,bot_id)
        client_bot = self.db_session.query(ClientBot).filter_by(client_id=int(client_id), bot_id=int(bot_id)).first()
    
        if client_bot:
                return client_bot.tkns_remaining
        return None 
        
    # def checkRemainingTokens(self, clientId, botId):
    #     client = Client.objects.get(id=clientId)
    #     for bot in client.bots:
    #         if bot.id == botId:
    #             return bot.tkns_remaining

    def getTokenCount(self, messages):
        """Returns the number of tokens used by a list of messages."""
        try:
            model = "gpt-3.5-turbo-0125"
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0125":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>
            return num_tokens
        else:
            raise NotImplementedError(f"""getTokenCount() is not presently implemented for model {model}.""")

    def moderate_content(self, apiToken, message):
        #OpenAI's Moderation API to check content
        url = "https://api.openai.com/v1/moderations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {apiToken}"
        }
        data = {"input": message}

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if response.status_code == 200:
            flagged = result["results"][0]["flagged"]
            categories = result["results"][0]["categories"]
            print({"flagged": flagged, "categories": categories})
            return {"flagged": flagged, "categories": categories}
        else:
            raise Exception(f"Moderation API Error: {result}")