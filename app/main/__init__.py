from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from .controllers.client_controller import client_blueprint 
from .controllers.bot_controller import bot_blueprint 
from .controllers.llm_controller import llm_blueprint, register_socketio_handlers
from .config import Config
from flask_migrate import Migrate

# Initialize SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()

# Initialize SocketIO
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register Blueprints
    app.register_blueprint(llm_blueprint, url_prefix='/llm')
    app.register_blueprint(client_blueprint, url_prefix='/client')
    app.register_blueprint(bot_blueprint, url_prefix='/bot')

    # Initialize SQLAlchemy with the app
    db.init_app(app)
    # migrate.init_app(app, db)
    
    # Register SocketIO handlers
    register_socketio_handlers(socketio)
    
    # Initialize SocketIO with the app
    socketio.init_app(app)

    return app


# from flask import Flask
# # from flask_mongoengine import MongoEngine
# from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from .controllers.client_controller import client_blueprint 
# from .controllers.bot_controller import bot_blueprint 
# from .controllers.llm_controller import llm_blueprint, register_socketio_handlers
# from .config import Config

# # db = MongoEngine()
# db = SQLAlchemy()

# socketio = SocketIO(cors_allowed_origins="*")

# def create_app():
#     app = Flask(__name__)

#     # Loading configuration
#     app.config.from_object(Config)
    
#     CORS(app, resources={r"/*": {"origins": "*"}})

#     app.register_blueprint(llm_blueprint, url_prefix='/llm')
#     app.register_blueprint(client_blueprint, url_prefix='/client')
#     app.register_blueprint(bot_blueprint, url_prefix='/bot')

#     # Initialize MongoDB
#     db.init_app(app)
    
#     register_socketio_handlers(socketio)
    
#     socketio.init_app(app)


#     return app
