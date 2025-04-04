# backend/config/settings.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DAILY_DB_ID = os.getenv("NOTION_DAILY_DB_ID")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Changed from XAI_API_KEY
    MT5_LOGIN = int(os.getenv("MT5_LOGIN"))
    MT5_PASSWORD = os.getenv("MT5_PASSWORD")
    MT5_SERVER = os.getenv("MT5_SERVER")

settings = Settings()