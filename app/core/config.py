import os
from dotenv import load_dotenv
from typing import Optional
import time
from datetime import datetime

load_dotenv()

class Settings:
    def __init__(self):
        self.__bot_token: Optional[str] = None
        self.__db_url: Optional[str] = None
        self.__api_secret: Optional[str] = None;
        self.__load_environment()
        self.__unixtimestamp: Optional[int] = None

    def __load_environment(self):
        self.__bot_token = os.environ.get("BOT_TOKEN")
        self.__db_url = os.environ.get("DB_URL")
        self.__api_secret = os.environ.get("API_SECRET")

    @property
    def unixtimestamp(self) -> int:
        self.__unixtimestamp = int(time.mktime(datetime.timetuple(datetime.now())))
        if self.__unixtimestamp is None:
            raise ValueError("unixtimestamp is not set")
        return self.__unixtimestamp
    
    @property
    def bot_token(self) -> str:
        if self.__bot_token is None:
            raise ValueError("BOT_TOKEN is not set in environment variables")
        return self.__bot_token

    @property
    def db_url(self) -> str:
        if self.__db_url is None:
            raise ValueError("DB_URL is not set in environment variables")
        return self.__db_url  
    @property
    def api_secret(self) -> str:
        if self.__api_secret is None:
            raise ValueError("Api secret is not set")
        return self.__api_secret
    
    @property
    def admin_secret_key(self) -> str:
        key = os.environ.get("ADMIN_SECRET_KEY")
        if not key:
            raise ValueError("ADMIN_SECRET_KEY not set")
        return key
    

settings = Settings()
