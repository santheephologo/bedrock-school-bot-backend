import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ASSISTANT_ID = os.environ.get('ASSISTANT_ID')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL')
    
    #DB config
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:@localhost/edubot'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MONGODB_SETTINGS = {
    #     'host': "mongodb://localhost:27017/schoolbot"
    # }