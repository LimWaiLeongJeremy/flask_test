import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'a_default_secret_key'
    # Example MySQL connection string 
    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:example@dbMySQL:3306/mydatabase'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'default_jwt_secret_key'
    
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


    

class TestingConfig(Config):
    TESTING = True 
    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:example@dbMySQL:3306/mydatabase'
    
    
class ProductionConfig(Config):
    DEBUG = False 
    SQLALCHEMY_ECHO = False
    