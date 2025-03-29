# backend/config/settings.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MT5_LOGIN = os.getenv("MT5_LOGIN")
    MT5_PASSWORD = os.getenv("MT5_PASSWORD")
    MT5_SERVER = os.getenv("MT5_SERVER")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DAILY_DB_ID = os.getenv("NOTION_DAILY_DB_ID")  # Your Daily database ID
    XAI_API_KEY = os.getenv("XAI_API_KEY")

settings = Settings()