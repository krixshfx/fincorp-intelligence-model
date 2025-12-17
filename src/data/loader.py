import yfinance as yf
import pandas as pd
from typing import Optional

class DataLoader:
    """
    Handles data ingestion from external sources like Yahoo Finance.
    """
    
    @staticmethod
    def fetch_stock_data(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Fetches historical stock data for a given ticker.
        
        Args:
            ticker (str): Stock symbol (e.g., 'AAPL').
            period (str): Data period (e.g., '1y', '5y', 'max').
            interval (str): Data interval (e.g., '1d', '1wk', '1mo').
            
        Returns:
            pd.DataFrame: Historical data with columns [Open, High, Low, Close, Volume, etc.]
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                raise ValueError(f"No data found for ticker symbol '{ticker}'")
                
            # Reset index to make Date a column
            df.reset_index(inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()

    @staticmethod
    def fetch_company_info(ticker: str) -> dict:
        """
        Fetches fundamental data for a company.
        """
        try:
            stock = yf.Ticker(ticker)
            return stock.info
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return {}
