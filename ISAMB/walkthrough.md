# ISAMB Walkthrough

The ISA Management Bot (ISAMB) has been implemented as a semi-automated system running on GitHub Actions.

## Implemented Components

1.  **Core Logic (`ISAMB/modules/`)**:
    -   `google_sheets.py`: Handles reading/writing to your Google Sheet.
    -   `market_data.py`: Fetches current prices using `finance-datareader` (KRX) and `yfinance` (US).
    -   `calculator.py`: Calculates portfolio value, rebalancing limits, and ISA tax simulations.
    -   `reporter.py`: Generates the text for Telegram messages.
    -   `telegram_bot.py`: Sends messages via Telegram API.

2.  **Configuration (`ISAMB/config/`)**:
    -   `settings.py`: Asset limits, tax rates, and thresholds.
    -   `secrets.py`: Securely loads API keys from environment variables.

3.  **Automation (`.github/workflows/isamb_schedule.yml`)**:
    -   Runs every **Saturday at 09:00 KST**.
    -   **Quarterly**: Checks if it's the first week of Jan, Apr, Jul, Oct for Rebalancing.
    -   **Bi-weekly**: Checks week number for routine Reminders.

## How to Start

Please refer to [ISAMB/SETUP.md](file:///home/chaehwan/Retirement-Pension-Management-Bot/ISAMB/SETUP.md) for detailed instructions on:
1.  Creating the Google Sheet.
2.  Setting up GitHub Secrets (`GOOGLE_SERVICE_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`).
