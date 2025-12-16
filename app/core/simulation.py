import numpy as np
import pandas as pd
from typing import Tuple, List

class MonteCarloSimulator:
    """
    Performs Monte Carlo simulations to forecast future price paths and risk.
    """
    
    @staticmethod
    def simulate_future_prices(
        start_price: float, 
        mu: float, 
        sigma: float, 
        days: int = 252, 
        simulations: int = 1000
    ) -> np.ndarray:
        """
        Simulates future stock prices using Geometric Brownian Motion (GBM).
        
        Args:
            start_price (float): The current stock price.
            mu (float): Annualized expected return (drift).
            sigma (float): Annualized volatility.
            days (int): Number of days to simulate.
            simulations (int): Number of simulation paths.
            
        Returns:
            np.ndarray: Array of shape (days, simulations) containing simulated prices.
        """
        dt = 1 / 252  # Time step (1 day)
        
        # Random component: epsilon ~ N(0, 1)
        # We generate all random shocks at once
        shock = np.random.normal(0, 1, (days, simulations))
        
        # Drift and Diffusion components
        drift = (mu - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * shock
        
        # Calculate daily returns
        daily_log_returns = drift + diffusion
        
        # Calculate price paths
        # We use cumsum to get cumulative log returns, then exp to get price multipliers
        price_paths = np.zeros((days, simulations))
        price_paths[0] = start_price
        
        for t in range(1, days):
            price_paths[t] = price_paths[t-1] * np.exp(daily_log_returns[t])
            
        return price_paths

    @staticmethod
    def get_simulation_stats(price_paths: np.ndarray) -> dict:
        """
        Calculates statistics from the simulation results.
        """
        final_prices = price_paths[-1]
        
        return {
            "mean_price": np.mean(final_prices),
            "median_price": np.median(final_prices),
            "min_price": np.min(final_prices),
            "max_price": np.max(final_prices),
            "percentile_5": np.percentile(final_prices, 5),
            "percentile_95": np.percentile(final_prices, 95)
        }
