from flask import Blueprint, jsonify,  request
from main.services.bot_service import BotService

bot_blueprint = Blueprint('bot', __name__)

bot_service = BotService()

@bot_blueprint.route('/')
def index():
    return 'bot Controller Working'

@bot_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    assistant_id = data.get('assistant_id')
    # agent_id = data.get('agent_id')
    # alias_id = data.get('alias_id')

    if not name or not assistant_id:
        return jsonify({"error": "Invalid data provided"}), 422
    try:
        response = bot_service.botRegister(name, assistant_id)
        if response is not None:
            return jsonify({"success": "Bot added"}), 201
        else:
            return jsonify({"error": "Bot name already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bot_blueprint.route('/fetch/db', methods=['GET'])
def fetch_dashboard_counts():
    try:
        response = bot_service.fetchDashboard()
        if response is not None:
            print("response ", response)
            return jsonify(response), 200
        else:
            return jsonify({"error": "Something went wrong"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bot_blueprint.route('/fetch', methods=['GET'])
def fetch_bots():
    try:
        response = bot_service.fetchBots()
        if response is not None:
            return jsonify(response), 200
        else:
            return jsonify({"error": "Something went wrong"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bot_blueprint.route('/bot/<name>', methods=['GET'])
def get_bot(name):
    try:
        response = bot_service.returnBot(name)
        if response is None:
            return jsonify({"error": "Bot not found"}), 404
        else:
            return jsonify(response.to_json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@bot_blueprint.route('/delete', methods=['PUT'])
def delete_bot():
    try:
        data = request.json
        botId = data.get('bot_id')
        response = bot_service.deleteBot(botId)
        if response is None:
            return jsonify({"error": "Bot not found"}), 404
        else:
            return jsonify({"success": "Deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bot_blueprint.route('/update', methods=['PUT'])
def update_bot():
    data = request.json
    name = data.get('name')
    bot_id = data.get('bot_id')
    assistant_id = data.get('assistant_id')
    # agent_id = data.get('agent_id')
    # alias_id = data.get('alias_id')

    if not name or not bot_id or not assistant_id:
        return jsonify({"error": "Invalid data provided"}), 400
    try:
        response = bot_service.updateBot(name, bot_id, assistant_id)
        if response is not None:
            return jsonify("Success ","updated"), 200
        else:
            return jsonify({"error": "Bot name already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bot_blueprint.route('/bot/update', methods=['PUT'])
def update_token():
    try:
        data = request.json
        username = data.get('username')
        add_tkn = data.get('add_tkn')
        if not username or add_tkn is None :
            return jsonify({"error": "Invalid input data"}), 400
        response = client_service.updateClientToken(username, add_tkn)
        if response is None:
            return jsonify({"error": "User not found"}), 404                   
        else:
            return jsonify({"success": "Token update success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bot_blueprint.route('/delete', methods=['Delete'])
def delete_client():
    try:
        data = request.json
        botId = data.get('botId')
        if botId is None:
            return jsonify({"error": "Invalid input data"}), 400
        response = bot_service.deleteBot(botId)
        if response is None:
            return jsonify({"error": "Bot not found"}), 404
        else:
            return jsonify({"success": "Bot deletion success"}), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

