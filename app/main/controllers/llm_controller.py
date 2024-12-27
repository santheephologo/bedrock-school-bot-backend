from flask import Blueprint, jsonify, request, current_app
from main.services.llm_service import LLMService
from main.services.chat_service import ChatService
from flask_socketio import SocketIO, emit, join_room, leave_room

llm_blueprint = Blueprint('llm', __name__)

llm_service = LLMService()
chat_service = ChatService()

@llm_blueprint.route('/')
def index():
    return 'LLM Controller Working'

#web socket implementation
def register_socketio_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('new client connection established')
    
    @socketio.on('get_chat_list')
    def handle_chat_list(data):
        try:
            session_id_prefix = data.get('session_id_prefix')
            if not session_id_prefix:
                emit('chat_list', "session_id_prefix required")
            else:
                chat_histories = chat_service.listChats(session_id_prefix)
                if not chat_histories:
                    emit('chat_list', "Empty here")
                else:
                    print('chat_list', chat_histories)
                    emit('chat_list', chat_histories)
        except Exception as e:
            emit('chat_list', str(e))

    @socketio.on('fetch_chat_history')
    def handle_chat_history(data):
        try:
            session_id = data.get('session_id')
            if not session_id:
                emit('fetched_chat_history', "Session id required")
            else:
                chat_histories = chat_service.getMessage(session_id)
                if not chat_histories:
                    emit('fetched_chat_history', "")
                else:
                    # print("final response : ", chat_histories)
                    emit('fetched_chat_history', chat_histories)
        except Exception as e:
            emit('fetched_chat_history', str(e))
                
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('message')
    def handle_message(data):
        try:
            print('msg received ', data)
            clientId = data.get('client_id')
            botId = data.get('bot_id')
            message = data.get('message')
            sessionId = data.get("session_id")
            
            if not clientId or not message or not botId or sessionId is None:
                emit('response', "Something went wrong")
            if message and clientId:
                if sessionId == "":
                    sessionId = chat_service.createNewChat(clientId, botId)
                    print(sessionId)
                    chat_histories = chat_service.listChats(f'{clientId}_{botId}')
                    emit('chat_list', chat_histories)
                print("session id ", sessionId)
                threadId = chat_service.getThreadId(session_id=sessionId)
                print("thread id ", threadId)
                response = llm_service.connectModel( message, clientId, botId, sessionId, threadId)
                print("resp final ", response)
                if response.get("error"):
                    print('response at 73 ',response)
                    emit('response', {"reply":response['error'], "session_id": sessionId})
             
                else:
                    chat_service.storeMessage(sessionId, message, response['message'])
                    print('response', response)
                    emit('response', {"reply":response['message'], "session_id": sessionId})
                    
        except Exception as e:
            emit('response', str(e))     

# @openai_blueprint.route('/convo', methods=['POST'])
# def convo():
   
#     try:
#         if request.method == "POST":
#             clientId = request.json.get('client_id')
#             message = request.json.get('message')

#             if not clientId or message is None:
#                 return jsonify({"error": "Invalid input data"}), 400
#             if message and clientId:
#                 response = openai_service.connectAi(message, clientId)
#                 if response.get("error"):
#                     return jsonify({"error": response["error"]}), 402       
#                 else:
#                     # print("response :", response)
#                     return jsonify(response), 200        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500