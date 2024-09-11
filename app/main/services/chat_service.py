from flask import jsonify
from main.models.chat_history import ChatHistory
import datetime


class ChatService:
    def storeMessage(self, session_id, req_message, res_message):
        try:
            print("running store msg ", session_id, req_message, res_message)
            chat_history = ChatHistory.objects.get(username=session_id)
            print("chat_history ", chat_history)
            # Add both user and bot messages to the ChatHistory document
            chat_history.add_message(req_message, "User")
            chat_history.add_message(res_message, "Bot")
            
            # Save the updated ChatHistory document
            chat_history.save()
            print("history saved")
            print(chat_history)
            return chat_history
        except Exception:
            return None

    def createNewChat(self, username):
        try:
            # Append the current date and time to the username
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_username = f"{username}_{timestamp}"
            
            chat_history = ChatHistory(username=formatted_username)
            chat_history.save()
            print(formatted_username)
            return formatted_username
        except Exception as e:
            print(f"Error creating new chat: {e}")
            return None
    
    def getMessage(self, session_id):
        try:
            # print("running get msg")
            chat_history = ChatHistory.objects.get(username=session_id)
            chats = self.listChats(session_id.split("_")[0])
            print("chat history ", chat_history.messages)
            all_messages = []
            for message in chat_history.messages:
                message_dict = message.to_json()
                all_messages.append(message_dict)
            
            # all_messages.reverse()    
            # print("all msgs ", all_messages)
            
            return {
                "chat_history":all_messages,
                "chat_list":chats
            }
        except Exception:
            return None

    def listChats(self, username_prefix):
        try:
            chats = ChatHistory.objects(username__startswith=username_prefix)
            
            results = []
            for chat in chats:
                if chat.messages:
                    first_message = chat.messages[0]['message']
                    results.append({
                        "username": chat.username,
                        "msg": first_message
                    })
            results.reverse()
            print(results)
            return results
            
        except Exception as e:
            print(f"Error: {e}")
            return None
