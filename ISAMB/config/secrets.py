import os

def get_google_service_key():
    return os.environ.get("GOOGLE_SERVICE_KEY")

def get_telegram_bot_token():
    return os.environ.get("TELEGRAM_BOT_TOKEN")

def get_telegram_chat_id():
    return os.environ.get("TELEGRAM_CHAT_ID")
