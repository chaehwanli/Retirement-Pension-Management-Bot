# Implementation Plan - ISA Management Bot (ISAMB)

This plan outlines the steps to build the semi-automated ISA Management Bot as described in `ISAMB/README.md`. The bot will run via GitHub Actions on a schedule, reading data from Google Sheets, updating prices, performing analysis, and sending reports via Telegram and GitHub Wiki.

## User Review Required
> [!IMPORTANT]
> **Google Sheets Structure**: The plan assumes specific sheet names ('Dashboard', 'Portfolio', 'ISA_Info', 'Simulation'). You will need to create these sheets in your Google Workbook before running the bot.
> **Credentials**: You must provide `GOOGLE_SERVICE_KEY` (JSON) and `TELEGRAM_BOT_TOKEN` as GitHub Secrets.

## Proposed Changes

### Project Structure
New directory `ISAMB/` will be the root for this specific bot.

```
ISAMB/
├── config/
│   ├── settings.py       # Configuration (ISA limits, Dates, Thresholds)
│   └── secrets.py        # Environment variable loader
├── modules/
│   ├── google_sheets.py  # Gspread integration (Read/Update)
│   ├── market_data.py    # Finance-datareader/Yfinance wrapper
│   ├── calculator.py     # ISA Simulation & Rebalancing logic
│   ├── reporter.py       # Report generation (Text/Markdown)
│   ├── telegram_bot.py   # Telegram notification
│   └── wiki_publisher.py # GitHub Wiki update
├── main.py               # Entry point (CLI args for mode: reminder/rebalancing)
├── requirements.txt      # Dependencies
└── README.md             # (Existing)
.github/
└── workflows/
    └── isamb_schedule.yml # CRON schedules
```

### [New] Core Modules

#### [NEW] [config/settings.py](file:///home/chaehwan/Retirement-Pension-Management-Bot/ISAMB/config/settings.py)
- Define ISA constraints (Start date: 2024-11-24, Limit: 60M, Obligation: 3yr).
- Define Target Allocation & Rebalancing thresholds.
- Define Sheet Names and Column mappings.

#### [NEW] [modules/google_sheets.py](file:///home/chaehwan/Retirement-Pension-Management-Bot/ISAMB/modules/google_sheets.py)
- `connect()`: Authenticate using Service Account.
- `get_portfolio_data()`: Read 'Portfolio' sheet.
- `update_current_prices(price_dict)`: Batch update '현재가' column.
- `update_dashboard(stats)`: Update 'Dashboard' sheet.
- `update_simulation(projection)`: Update 'Simulation' sheet.

#### [NEW] [modules/market_data.py](file:///home/chaehwan/Retirement-Pension-Management-Bot/ISAMB/modules/market_data.py)
- `fetch_prices(ticker_list)`: Use `finance-datareader` (KRX) and `yfinance` (US) to get latest close prices.

#### [NEW] [modules/calculator.py](file:///home/chaehwan/Retirement-Pension-Management-Bot/ISAMB/modules/calculator.py)
- `calculate_portfolio_stats()`: Total Value, Profit, Yield.
- `check_rebalancing_needed(current_weights, target_weights)`: Compare against thresholds.
- `simulate_isa_maturity()`: Calculate tax-free limit (2M), excess tax (9.9%), and final payout.

#### [NEW] [modules/reporter.py](file:///home/chaehwan/Retirement-Pension-Management-Bot/ISAMB/modules/reporter.py)
- `generate_reminder_message()`: "Please update sheets..." + Brief Summary.
- `generate_rebalancing_report()`: Detailed markdown report.

#### [NEW] [modules/telegram_bot.py](file:///home/chaehwan/Retirement-Pension-Management-Bot/ISAMB/modules/telegram_bot.py)
- `send_message(chat_id, text)`: Send alerts.

#### [NEW] [main.py](file:///home/chaehwan/Retirement-Pension-Management-Bot/ISAMB/main.py)
- Argument Parser: `--mode` (`reminder`, `rebalancing`).
- Workflow:
    1. Load Config.
    2. Connect Sheets.
    3. Fetch & Update Prices.
    4. Calculate Stats.
    5. If `reminder`: Send simple alert.
    6. If `rebalancing`: Run deep analysis & Send detailed report.

### [New] Automation

#### [NEW] [.github/workflows/isamb_schedule.yml](file:///home/chaehwan/Retirement-Pension-Management-Bot/.github/workflows/isamb_schedule.yml)
- **Schedule 1 (Bi-weekly Reminder):** `0 0 * * 6` (Example check, logic inside script to filter for bi-weekly). *Correction*: CRON syntax for "Every 2nd Saturday" is tricky; better to run every Saturday and check date in Python, OR use specific dates.
    - *Plan*: Run every Saturday 00:00 UTC (9:00 KST). Python script decides if it's a "Reminder Week" or "Rebalancing Week".
- **Jobs**: Install Python, Install Deps, Run `main.py`.

## Verification Plan

### Automated Tests
- Create `tests/test_calculator.py` to verify tax and rebalancing math.
- Mock Google Sheets API to test data parsing.

### Manual Verification
- **Dry Run**: Run `main.py` locally with `--mode reminder` and `--mode rebalancing`.
    - Check if Google Sheet 'Portfolio' updates prices.
    - Check if Telegram message is received.
    - Check if Wiki is updated (if implemented).
