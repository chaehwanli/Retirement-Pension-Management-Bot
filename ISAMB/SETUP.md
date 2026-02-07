# ISAMB Setup Guide

## 1. Google Sheets Setup
Create a new Google Sheet named **"ISA_관리"** (or change `SHEET_NAME` in `config/settings.py`).
Create the following sheets inside it:

### Sheet 1: `Dashboard`
(Optional structure, bot will try to update specific cells if defined)

### Sheet 2: `Portfolio`
The bot reads from this sheet. Make sure the following columns exist (in row 1):
- **종목명** (Name)
- **티커** (Ticker) - crucial! (e.g., `005930`, `TSLA`)
- **보유수량** (Quantity) - You must update this manually.
- **매수단가** (Avg Price)
- **현재가** (Current Price) - **Bot will update this column.**
- **수익률** (Yield) - Can be formula `= (E2-D2)/D2`.
- **비중** (Weight) - Can be formula `= (E2*C2)/SUM(...)`.
- **Target_Weight** (Optional) - If you want rebalancing suggestions, add this column with decimal values (e.g., 0.1 for 10%).

### Sheet 3: `ISA_Info`
(Optional, for static info)

### Sheet 4: `Simulation`
The bot will append simulation results here if implemented.

---

## 4. How to Manage Cash (Deposit Limit)
User feedback indicates cash should be treated as **Deposit (Liquidity Pool)** rather than a rebalancing target.

### 1️⃣ Tracking Cash (예수금 현황)
*   **Item Name**: `현금` or `예수금`
*   **Ticker**: `CASH` or `KRW`
*   **Quantity**: Amount in KRW.
*   **Target_Weight**: **LEAVE EMPTY or 0**.
    *   The bot will **NOT** suggest BUY/SELL for Cash.
    *   It will simply report the total cash amount as "Deposit" in the report.
    *   This cash is included in the "Total Asset Value" calculation which affects the weight percentage of other assets.

### 2️⃣ Setting Target Weights (Stocks/ETFs)
*   Set `Target_Weight` for your assets (e.g., Samsung: 0.5, S&P500: 0.5).
*   The sum of targets for **Assets** can be 1.0 (100%).
*   The bot will tell you to Buy/Sell stocks based on their value relative to the (Asset + Cash) total, but will assume Cash is the funding source/destination.

## 2. Secrets Configuration (GitHub Actions)
Go to your Repository -> Settings -> Secrets and variables -> Actions -> New repository secret.
Add the following:

1.  **GOOGLE_SERVICE_KEY**: The content of your Google Service Account JSON key.
    - *Note*: Ensure the Service Account email has **Editor** access to your Google Sheet.
2.  **TELEGRAM_BOT_TOKEN**: Your Telegram Bot API token.
3.  **TELEGRAM_CHAT_ID**: Your Telegram Chat ID (where the bot sends messages).

4.  **(Optional) Multiple Recipients**:
    - To send messages to additional users (e.g., spouse), add:
    - `TELEGRAM_BOT_TOKEN_1`, `TELEGRAM_CHAT_ID_1`
    - `TELEGRAM_BOT_TOKEN_2`, `TELEGRAM_CHAT_ID_2`
    - You can add up to 5 additional recipients (suffixes `_1` to `_5`).

## 3. Local Execution (Testing)
1.  Create a `.env` file in `ISAMB/` with the above secrets (for local testing).
2.  Run:
    ```bash
    pip install -r ISAMB/requirements.txt
    python ISAMB/main.py --mode reminder
    ```
