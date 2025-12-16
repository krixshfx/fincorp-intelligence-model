import pandas as pd
import numpy as np

class RiskAnalyzer:
    """
    Calculates enterprise risk metrics.
    """
    
    @staticmethod
    def calculate_volatility(daily_returns: pd.Series, annualized: bool = True) -> float:
        """Calculates volatility (standard deviation of returns)."""
        vol = daily_returns.std()
        if annualized:
            vol *= np.sqrt(252)
        return vol

    @staticmethod
    def calculate_max_drawdown(df: pd.DataFrame) -> float:
        """
        Calculates Maximum Drawdown (MDD).
        MDD = Min((Price - Peak) / Peak)
        """
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column")
            
        prices = df['Close']
        rolling_max = prices.cummax()
        drawdown = (prices - rolling_max) / rolling_max
        return drawdown.min()

    @staticmethod
    def calculate_var(daily_returns: pd.Series, confidence_level: float = 0.95) -> float:
        """
        Calculates Value at Risk (VaR) using the parametric method.
        """
        mean = daily_returns.mean()
        std = daily_returns.std()
        
        # Z-score for confidence level (e.g., 1.65 for 95%)
        from scipy.stats import norm
        z_score = norm.ppf(1 - confidence_level)
        
        var = mean + z_score * std
        return var # This is the return threshold

    @staticmethod
    def calculate_historical_var(daily_returns: pd.Series, confidence_level: float = 0.95) -> float:
        """
        Calculates Value at Risk (VaR) using historical simulation.
        """
        return daily_returns.quantile(1 - confidence_level)
