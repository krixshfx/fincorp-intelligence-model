# Enterprise Risk & Financial Performance Intelligence System

## 🚀 Overview
A high-performance financial analytics platform designed for **quantitative analysis**, **risk management**, and **investment research**. This system provides institutional-grade insights into asset performance, volatility modeling, and market risk exposure.

Built with a modular architecture, it separates core quantitative logic from data ingestion and visualization layers, demonstrating scalable software engineering practices suitable for enterprise fintech environments.

## 🌟 Key Features
- **Advanced Risk Metrics**: 
  - Value at Risk (VaR) Calculation (Parametric & Historical).
  - Volatility Modeling (Annualized Standard Deviation).
  - Maximum Drawdown (MDD) Analysis.
- **Performance Attribution**:
  - Sharpe Ratio & Risk-Adjusted Returns.
  - CAGR (Compound Annual Growth Rate).
  - Alpha/Beta Sensitivity (Planned).
- **Predictive Analytics (New!)**:
  - **Monte Carlo Simulation**: Geometric Brownian Motion (GBM) for future price path forecasting.
  - Risk Scenarios: Best/Worst case estimation (5th/95th percentile).
- **Interactive Visualization**:
  - Institutional-grade dashboards using **Streamlit** & **Plotly**.
  - Dynamic time-series analysis (Candlestick, Volume).
  - Return distribution histograms.
- **Modern Tech Stack**:
  - **Backend**: Python 3.10+, FastAPI (for API services).
  - **Frontend**: Streamlit (Analyst Mode).
  - **Data**: Yahoo Finance API (yfinance), Pandas, NumPy.

## 🏗️ Architecture
The project follows a Domain-Driven Design (DDD) approach:

```
financial_intelligence_system/
├── app/
│   ├── core/           # Domain Logic (Quant Algorithms)
│   ├── data/           # Data Access Layer (DAL)
│   ├── api/            # REST API (FastAPI)
│   └── ui/             # Presentation Layer (Streamlit)
├── tests/              # Unit & Integration Tests
└── requirements.txt
```

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/financial-intelligence-system.git
   cd financial_intelligence_system
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

### Mode 1: Analyst Dashboard (UI)
Launch the interactive dashboard for visual analysis:
```bash
streamlit run app.py
```

### Mode 2: REST API (Headless)
Start the backend server for programmatic access:
```bash
uvicorn app.api.main:app --reload
```
Access Swagger Documentation at: `http://localhost:8000/docs`

## 📊 Methodology

### Sharpe Ratio
Calculated as $S_a = \frac{E[R_a - R_f]}{\sigma_a}$, where $R_f$ is the risk-free rate (default 2%).

### Value at Risk (VaR)
Estimates the maximum potential loss over a specified time frame with a given confidence interval (95%).
- **Parametric VaR**: Assumes normal distribution of returns.
- **Historical VaR**: Based on empirical percentile of historical returns.

## 🔮 Future Roadmap
- [ ] Integration with Bloomberg Terminal / FactSet APIs.
- [ ] Machine Learning for Price Prediction (LSTM/Transformer models).
- [ ] Portfolio Optimization (Markowitz Efficient Frontier).
- [ ] Sentiment Analysis using NLP on Financial News.

---
*Designed for Top-Tier Financial Institutions & Hedge Funds.*
