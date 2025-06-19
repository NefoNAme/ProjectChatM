from dotenv import load_dotenv
import os
load_dotenv()
class Config:
    DATABASE_USER = os.getenv('USER_NAME')
    DATABASE_NAME = os.getenv('NAME_DATABASE')
    DATABASE_PASSWORD = os.getenv('PASSWORD')
    DATABASE_HOST = os.getenv('IP_ADDRESS')
    DATABASE_PORT = os.getenv("PORT")