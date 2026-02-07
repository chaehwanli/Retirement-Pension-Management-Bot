
import requests
from config import secrets

class TelegramBot:
    def __init__(self):
        self.token = secrets.get_telegram_bot_token()
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def send_message(self, chat_id, text):
        """
        Sends a message to a specific chat ID.
        """
        if not self.token:
            print("Telegram Bot Token not found.")
            return

        url = self.base_url + "sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Message sent successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")
