# backend/config/settings.py
from dotenv import load_dotenv
import os

# Explicitly load .env from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", ".env"))

class Settings:
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DAILY_DB_ID = os.getenv("NOTION_DAILY_DB_ID")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MT5_LOGIN = int(os.getenv("MT5_LOGIN") or 0)  # Fallback if still None
    MT5_PASSWORD = os.getenv("MT5_PASSWORD")
    MT5_SERVER = os.getenv("MT5_SERVER")

settings = Settings()