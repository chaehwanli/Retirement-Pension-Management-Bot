import os

def get_google_service_key():
    return os.environ.get("GOOGLE_SERVICE_KEY")

def get_telegram_configs():
    """
    Returns a list of dictionaries: [{'token': '...', 'chat_id': '...'}]
    Supports single variables (TELEGRAM_BOT_TOKEN) and multiple (TELEGRAM_BOT_TOKEN_1, _2...)
    """
    configs = []
    
    # Check for primary/default env vars
    default_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    default_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if default_token and default_chat_id:
        configs.append({'token': default_token, 'chat_id': default_chat_id})
        
    # Check for numbered suffixes (e.g., _1, _2 up to 5)
    for i in range(1, 6):
        token = os.environ.get(f"TELEGRAM_BOT_TOKEN_{i}")
        chat_id = os.environ.get(f"TELEGRAM_CHAT_ID_{i}")
        if token and chat_id:
            configs.append({'token': token, 'chat_id': chat_id})
            
    return configs
