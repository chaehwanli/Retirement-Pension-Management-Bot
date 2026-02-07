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

## 4. How to Manage Cash & Rebalancing
To enable proper rebalancing and cash management, follow these rules in your **Portfolio** sheet:

### 1️⃣ Managing Cash for Buying (예수금 관리)
*   **Item Name (종목명)**: `현금` or `예수금`
*   **Ticker (티커)**: `CASH` or `KRW` (Must use one of these exactly!)
*   **Quantity (보유수량)**: Enter the actual amount of cash in KRW (e.g., `5000000`).
*   **Avg Price (매수단가)**: `1`
*   **Current Price (현재가)**: `1` (The bot will strictly maintain this as 1).

### 2️⃣ Setting Target Weights (비중 지정)
*   Use the **`Target_Weight`** column.
*   Enter values as **decimals** (e.g., `0.3` for 30%).
*   **Important**: The sum of all `Target_Weight` values (including CASH) should equal **1.0** (100%).
    *   Example:
        *   Samsung Electronics: `0.4` (40%)
        *   S&P 500 ETF: `0.4` (40%)
        *   CASH: `0.2` (20%)
*   If the sum is not 1.0, the bot will still calculate rebalancing based on the relative weights provided, but it's best practice to match 100%.

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
