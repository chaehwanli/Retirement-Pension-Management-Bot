
import FinanceDataReader as fdr
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class MarketDataFetcher:
    def __init__(self):
        pass

    def get_price(self, ticker):
        """
        Fetches the latest closing price for a given ticker.
        """
        try:
            # Check if it's a Korean stock (6 digits)
            if ticker.isdigit() and len(ticker) == 6:
                df = fdr.DataReader(ticker, datetime.now() - timedelta(days=7))
                if not df.empty:
                    return df['Close'].iloc[-1]
                else:
                    return None
            else:
                # Assume US stock or ETF
                ticker_obj = yf.Ticker(ticker)
                # Try to get fast info first
                try:
                    price = ticker_obj.info.get('regularMarketPrice')
                    if price:
                         return price
                except:
                    pass
                
                # Fallback to history
                df = ticker_obj.history(period="5d")
                if not df.empty:
                    return df['Close'].iloc[-1]
                else:
                    return None

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    def get_prices(self, tickers):
        """
        Fetches prices for a list of tickers.
        Returns a dictionary {ticker: price}.
        """
        prices = {}
        for ticker in tickers:
            price = self.get_price(ticker)
            if price:
                prices[ticker] = price
            else:
                print(f"Failed to fetch price for {ticker}")
        return prices
