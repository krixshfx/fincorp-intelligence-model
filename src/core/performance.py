import pandas as pd
import numpy as np

class PerformanceAnalyzer:
    """
    Calculates financial performance metrics.
    """
    
    @staticmethod
    def calculate_daily_returns(df: pd.DataFrame) -> pd.Series:
        """Calculates daily percentage change."""
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column")
        return df['Close'].pct_change().dropna()

    @staticmethod
    def calculate_cumulative_returns(df: pd.DataFrame) -> pd.Series:
        """Calculates cumulative returns over the period."""
        daily_returns = PerformanceAnalyzer.calculate_daily_returns(df)
        return (1 + daily_returns).cumprod() - 1

    @staticmethod
    def calculate_sharpe_ratio(df: pd.DataFrame, risk_free_rate: float = 0.02) -> float:
        """
        Calculates annualized Sharpe Ratio.
        Assumes 252 trading days.
        """
        daily_returns = PerformanceAnalyzer.calculate_daily_returns(df)
        mean_return = daily_returns.mean()
        std_dev = daily_returns.std()
        
        if std_dev == 0:
            return 0.0
            
        # Annualize
        sharpe = (mean_return * 252 - risk_free_rate) / (std_dev * np.sqrt(252))
        return sharpe

    @staticmethod
    def calculate_cagr(df: pd.DataFrame) -> float:
        """Compound Annual Growth Rate."""
        if df.empty:
            return 0.0
            
        start_price = df['Close'].iloc[0]
        end_price = df['Close'].iloc[-1]
        
        # Calculate number of years (approximate)
        days = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days
        years = days / 365.25
        
        if years == 0:
            return 0.0
            
        cagr = (end_price / start_price) ** (1 / years) - 1
        return cagr
