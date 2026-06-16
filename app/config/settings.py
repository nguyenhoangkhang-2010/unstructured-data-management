import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key_flask_mining')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DB_NAME = 'cv_mining_system'
    
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    ROOT_DIR = os.path.dirname(BASE_DIR)
    
    OUTPUT_FOLDER = os.path.join(ROOT_DIR, 'outputs')
    STATIC_OUTPUTS = os.path.join(BASE_DIR, 'static', 'outputs')