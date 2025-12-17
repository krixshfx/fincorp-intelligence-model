from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import pandas as pd

from app.data.loader import DataLoader
from app.core.performance import PerformanceAnalyzer
from app.core.risk import RiskAnalyzer

app = FastAPI(
    title="Financial Intelligence System API",
    description="Enterprise-grade financial data analysis and risk management API",
    version="1.0.0"
)

class AnalysisRequest(BaseModel):
    ticker: str
    period: str = "1y"
    interval: str = "1d"

class AnalysisResponse(BaseModel):
    ticker: str
    current_price: float
    volatility_annualized: float
    sharpe_ratio: float
    max_drawdown: float
    cagr: float
    value_at_risk_95: float
    company_info: Dict

@app.get("/")
async def root():
    return {"message": "Financial Intelligence System API is running"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    try:
        # 1. Fetch Data
        df = DataLoader.fetch_stock_data(request.ticker, request.period, request.interval)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {request.ticker}")

        # 2. Fetch Info
        info = DataLoader.fetch_company_info(request.ticker)

        # 3. Calculate Metrics
        daily_returns = PerformanceAnalyzer.calculate_daily_returns(df)
        
        volatility = RiskAnalyzer.calculate_volatility(daily_returns)
        max_dd = RiskAnalyzer.calculate_max_drawdown(df)
        var_95 = RiskAnalyzer.calculate_historical_var(daily_returns)
        
        sharpe = PerformanceAnalyzer.calculate_sharpe_ratio(df)
        cagr = PerformanceAnalyzer.calculate_cagr(df)
        
        current_price = df['Close'].iloc[-1]

        return AnalysisResponse(
            ticker=request.ticker,
            current_price=round(current_price, 2),
            volatility_annualized=round(volatility, 4),
            sharpe_ratio=round(sharpe, 4),
            max_drawdown=round(max_dd, 4),
            cagr=round(cagr, 4),
            value_at_risk_95=round(var_95, 4),
            company_info=info
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
