
import argparse
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings, secrets
from modules.google_sheets import GoogleSheetsManager
from modules.market_data import MarketDataFetcher
from modules.calculator import Calculator
from modules.reporter import Reporter
from modules.telegram_bot import TelegramBot

def main():
    parser = argparse.ArgumentParser(description="ISA Management Bot")
    parser.add_argument("--mode", type=str, choices=["reminder", "rebalancing"], required=True, help="Execution mode")
    args = parser.parse_args()

    # 1. Initialize Modules
    print("Initializing ISAMB...")
    
    # Load secrets
    service_key = secrets.get_google_service_key()
    telegram_token = secrets.get_telegram_bot_token()
    chat_id = secrets.get_telegram_chat_id()
    
    if not service_key or not telegram_token or not chat_id:
        print("Error: Missing environment variables (GOOGLE_SERVICE_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID).")
        return

    sheets_manager = GoogleSheetsManager(service_key)
    market_data = MarketDataFetcher()
    calculator = Calculator()
    reporter = Reporter()
    bot = TelegramBot()

    # 2. Fetch Data from Google Sheets
    print(f"Fetching data from '{settings.SHEET_NAME_PORTFOLIO}'...")
    portfolio_data = sheets_manager.get_sheet_data(settings.SHEET_NAME_PORTFOLIO)
    
    if not portfolio_data:
        print("Error: Failed to fetch portfolio data.")
        return

    # 3. Update Current Prices
    print("Updating current prices...")
    tickers = [item['티커'] for item in portfolio_data if item.get('티커')]
    prices = market_data.get_prices(tickers)
    
    # Update local data structure first
    for item in portfolio_data:
        ticker = item.get('티커')
        if ticker in prices:
            item['현재가'] = prices[ticker]
    
    # Update Google Sheet with new prices
    # Note: This requires mapping '현재가' to a column index. 
    # For now, let's assume '현재가' is a column name and use a helper if needed.
    # To be safe and efficient, let's update column-wise if the sheet structure is known.
    # For simplicity in this v1, we iterate rows (slow but safe) or just trust the local calculation for the report.
    # Better: Update the '현재가' column in the sheet.
    price_list = []
    for item in portfolio_data:
        # Re-match because dict order might vary? No, list order is preserved.
        price_list.append(item.get('현재가', 0))
    
    sheets_manager.update_column(settings.SHEET_NAME_PORTFOLIO, '현재가', price_list)

    # 4. Calculate Stats
    print("Calculating portfolio stats...")
    total_value, total_invested = calculator.calculate_total_value(portfolio_data)
    total_profit = total_value - total_invested
    
    # 5. Execute Logic based on Mode
    if args.mode == "reminder":
        print("Running in REMINDER mode...")
        message = reporter.generate_reminder_message(total_value, total_profit)
        bot.send_message(chat_id, message)
        
    elif args.mode == "rebalancing":
        print("Running in REBALANCING mode...")
        # Check rebalancing
        suggestions = calculator.check_rebalancing_needed(portfolio_data)
        
        # Simulation
        simulation_result = calculator.simulate_isa(total_profit)
        
        # Generate detailed report
        report = reporter.generate_rebalancing_report(portfolio_data, suggestions, simulation_result)
        bot.send_message(chat_id, report)
        
        # TODO: Wiki publishing can be added here
        
    print("ISAMB execution completed.")

if __name__ == "__main__":
    main()
