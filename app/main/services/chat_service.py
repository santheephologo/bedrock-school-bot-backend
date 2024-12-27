from sqlalchemy.orm import Session

from flask import current_app
from main.models.chat_history import ChatHistory
from main.models.message import Message    
from main.services.llm_service import LLMService
import datetime

class ChatService:
    
    def __init__(self):
        self.llm_service = LLMService()
        # pass
    
    @property
    def db_session(self):
        from main import db
        return db.session

    def storeMessage(self, session_id, req_message, res_message):
        try:
            print("Running store message", session_id, req_message, res_message)
            chat_history = self.db_session.query(ChatHistory).filter_by(session_id=session_id).first()
            print("Chat history found:", chat_history)

            if chat_history:
                print('type ', type(chat_history.messages))
                new_message1 = Message(req_message, "User")
                new_message2 = Message(res_message, "Bot")
                print('message1: ', new_message1.to_json())
                print('message2: ', new_message2.to_json())
                chat_history.messages.append(new_message1.to_json())
                chat_history.messages.append(new_message2.to_json())
                # self.db_session.add(chat_history)
                self.db_session.commit()
                print("History saved")
                print(chat_history)
                return chat_history
            return None
        except Exception as e:
            print(f"Error storing message: {e}")
            self.db_session.rollback() 
            return None

    def createNewChat(self, clientId, botId):
        try:
            
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_session_id = f"{clientId}_{botId}_{timestamp}"
            thread_id = self.llm_service.createThread(current_app.config['OPENAI_API_KEY'])
            chat_history = ChatHistory(thread_id=thread_id, session_id=formatted_session_id)
            self.db_session.add(chat_history)  
            self.db_session.commit() 
            print(formatted_session_id)
            return formatted_session_id
        
        except Exception as e:
            print(f"Error creating new chat: {e}")
            self.db_session.rollback()  
            return None
    def getThreadId(self, session_id):
        try:
            thread = self.db_session.query(ChatHistory).filter_by(session_id=session_id).first()
            return thread.thread_id if thread else None
        except Exception as e:
            print(f"Error fetching chat history: {e}")
            return None
    def getMessage(self, session_id):
        try:
            chat_history = self.db_session.query(ChatHistory).filter_by(session_id=session_id).first()
            parts = session_id.split("_")
            session_id_prefix = "_".join(parts[:2])
            chats = self.listChats(session_id_prefix)

            if chat_history:
                print("Chat history messages:", chat_history.messages)
                # all_messages = [message.to_json() for message in chat_history.messages]

                return {
                    "chat_history": chat_history.messages,
                    "chat_list": chats
                }
            return None
        except Exception as e:
            print(f"Error getting messages: {e}")
            return None

    def listChats(self, session_id_prefix):
        try:
            chats = self.db_session.query(ChatHistory).filter(ChatHistory.session_id.startswith(session_id_prefix)).all()
            # print('chats found ',chats)
            results = []
            for chat in chats:
                # print("chat ",chat.to_json())
                if chat.messages:
                    # print("msgs ", chat.messages)
                    first_message = chat.messages[0]['message']
                    results.append({
                        "session_id": chat.session_id,
                        "msg": first_message
                    })
            # print("Chat list results:", results)
            return results

        except Exception as e:
            print(f"Error listing chats: {e}")
            return None


# from flask import jsonify
# from main.models.chat_history import ChatHistory
# import datetime


# class ChatService:
#     def storeMessage(self, session_id, req_message, res_message):
#         try:
#             print("running store msg ", session_id, req_message, res_message)
#             chat_history = ChatHistory.objects.get(username=session_id)
#             print("chat_history ", chat_history)
#             # Add both user and bot messages to the ChatHistory document
#             chat_history.add_message(req_message, "User")
#             chat_history.add_message(res_message, "Bot")
            
#             # Save the updated ChatHistory document
#             chat_history.save()
#             print("history saved")
#             print(chat_history)
#             return chat_history
#         except Exception:
#             return None

#     def createNewChat(self, clientId, botId):
#         try:
#             # Append the current date and time to the username
#             timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             formatted_username = f"{clientId}_{botId}_{timestamp}"
            
#             chat_history = ChatHistory(username=formatted_username)
#             chat_history.save()
#             print(formatted_username)
#             return formatted_username
#         except Exception as e:
#             print(f"Error creating new chat: {e}")
#             return None
    
#     def getMessage(self, username):
#         try:
#             # print("running get msg")
#             chat_history = ChatHistory.objects.get(username=username)
#             parts = username.split("_")
#             client_bot_id = "_".join(parts[:2])
#             chats = self.listChats(client_bot_id)
#             print("chat history ", chat_history.messages)
#             all_messages = []
#             for message in chat_history.messages:
#                 message_dict = message.to_json()
#                 all_messages.append(message_dict)
            
#             # all_messages.reverse()    
#             # print("all msgs ", all_messages)
            
#             return {
#                 "chat_history":all_messages,
#                 "chat_list":chats
#             }
#         except Exception:
#             return None

#     def listChats(self, username_prefix):
#         try:
#             chats = ChatHistory.objects(username__startswith=username_prefix)
            
#             results = []
#             for chat in chats:
#                 if chat.messages:
#                     first_message = chat.messages[0]['message']
#                     results.append({
#                         "username": chat.username,
#                         "msg": first_message
#                     })
#             # results.reverse()
#             print(results)
#             return results
            
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
