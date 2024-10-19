from flask import Blueprint, jsonify,  request
from main.services.client_service import ClientService

client_blueprint = Blueprint('client', __name__)

client_service = ClientService()

@client_blueprint.route('/')
def index():
    return 'Token Controller Working'

@client_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('fname')
    last_name = data.get('lname')

    if not username or not email or not password or not first_name or not last_name :
        print (data)
        return jsonify({"error": "Invalid data provided"}), 400
    try:
        response = client_service.clientRegister(username,email,password,first_name,last_name )
        if response is not None:
            return jsonify({"success": "Client added"}), 201
        else:
            return jsonify({"error": "Username already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')    

    if not email or not password :
        return jsonify({"error": "Invalid data provided", }), 400
    try:
        response = client_service.clientLogin(email,password)

        if response is not None:
            if response:
                return jsonify({"success": "login success"}), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401
        else:
            return jsonify({"error": "User doesn't exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@client_blueprint.route('/fetch', methods=['GET'])
def fetch_clients():
    try:
        response = client_service.fetchClients()
        if response is not None:
            return jsonify(response), 200
        else:
            return jsonify({"error": "Something went wrong"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_blueprint.route('/<username>', methods=['GET'])
def get_user(username):
    try:
        response = client_service.returnClient(username)
        if response is None:
            return jsonify({"error": "User not found"}), 404
        else:
            return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@client_blueprint.route('/token/<username>', methods=['GET'])
def get_token(username):
    try:
        response = client_service.returnTokenInfo(username )
        if response is None:
            return jsonify({"error": "User not found"}), 404
        else:
            return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@client_blueprint.route('/token/update', methods=['PUT'])
def update_token():
    try:
        data = request.json
        client_id = data.get('client_id')
        bot_id = data.get('bot_id')
        add_tkn = data.get('add_tkn')
        if client_id is None or bot_id is None or add_tkn is None :
            return jsonify({"error": "Invalid input data"}), 400
        response = client_service.updateClientBotToken(client_id, bot_id, add_tkn)
        if response is None:
            return jsonify({"error": "User not found"}), 404                   
        else:
            return jsonify({"success": "Token update success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_blueprint.route('/unsubscribe', methods=['PUT'])
def delete_bot_from_client():
    try:
        data = request.json
        client_id = data.get('client_id')
        bot_id = data.get('bot_id')
        if client_id is None or bot_id is None :
            print(data)
            return jsonify({"error": "Invalid input data"}), 400
        response = client_service.deleteClientBot(client_id, bot_id)
        if response is None:
            return jsonify({"error": "User not found"}), 404                   
        else:
            return jsonify({"success": "unsubscribed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_blueprint.route('/bot/add', methods=['POST'])
def add_bot():
    try:
        data = request.json
        client_id = data.get('client_id')
        bot_name = data.get('bot_name')
        bot_id = data.get('bot_id')
        tkns_remaining = data.get('tkns_remaining')
        tkns_used = data.get('tkns_used')
        if client_id is None or bot_name is None or bot_id is None or tkns_remaining is None or tkns_used is None:
            print(data)
            return jsonify({"error": "Invalid input data"}), 400
        response = client_service.addBot(client_id, bot_name, bot_id, tkns_remaining, tkns_used)
        if response is None:
            return jsonify({"error": "User not found"}), 404                   
        else:
            return jsonify({"success": "bot added"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_blueprint.route('/delete', methods=['Delete'])
def delete_client():
    try:
        data = request.json
        clientId = data.get('clientId')
        if clientId is None:
            return jsonify({"error": "Invalid input data"}), 400
        response = client_service.deleteClient(clientId)
        if response is None:
            return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"success": "client deletion success"}), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

