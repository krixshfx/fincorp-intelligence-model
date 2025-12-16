import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    print("Testing Imports...")
    from app.data.loader import DataLoader
    from app.core.performance import PerformanceAnalyzer
    from app.core.risk import RiskAnalyzer
    from app.api.main import app
    print("Imports Successful.")

    # Test Data Loading (Mock if needed, but let's try real fetch for AAPL)
    print("Testing Data Fetch (AAPL)...")
    df = DataLoader.fetch_stock_data("AAPL", period="1mo", interval="1d")
    if not df.empty:
        print(f"Data Fetched: {len(df)} rows.")
        
        # Test Core Logic
        returns = PerformanceAnalyzer.calculate_daily_returns(df)
        vol = RiskAnalyzer.calculate_volatility(returns)
        sharpe = PerformanceAnalyzer.calculate_sharpe_ratio(df)
        print(f"Volatility: {vol:.4f}")
        print(f"Sharpe: {sharpe:.4f}")
    else:
        print("Warning: Data fetch returned empty (check internet).")

    print("Verification Complete.")

except Exception as e:
    print(f"Verification Failed: {e}")
    import traceback
    traceback.print_exc()
