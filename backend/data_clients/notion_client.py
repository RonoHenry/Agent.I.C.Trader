# backend/utils/notion_client.py
from notion_client import Client
from backend.config.settings import settings

def add_daily_entry(entry):
    notion = Client(auth=settings.NOTION_API_KEY)
    db_id = settings.NOTION_DAILY_DB_ID
    new_page = {
        "parent": {"database_id": db_id},
        "properties": {
            "Date": {"title": [{"text": {"content": entry["Date"]}}]},
            "Setup": {"rich_text": [{"text": {"content": entry["Setup"]}}]},
            "Outcome": {"select": {"name": entry["Outcome"]}}
        }
    }
    notion.pages.create(**new_page)

if __name__ == "__main__":
    print("Testing Notion API directly")
    try:
        entry = {
            "Date": "2025-04-07",
            "Setup": "Direct Test Setup",
            "Outcome": "Win"
        }
        add_daily_entry(entry)
        print("Notion entry added successfully")
    except Exception as e:
        print(f"Notion error: {e}")