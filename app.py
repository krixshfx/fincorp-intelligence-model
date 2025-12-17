import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add current directory to path so we can import app modules
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, SRC_PATH)

from src.data.loader import DataLoader
from src.core.performance import PerformanceAnalyzer
from src.core.risk import RiskAnalyzer
from src.core.simulation import MonteCarloSimulator

st.set_page_config(page_title="Financial Analyst Mode", layout="wide", page_icon="📈")

# --- CSS Styling ---
st.markdown("""
<style>
    .metric-card {
        background-color: #0e1117;
        border: 1px solid #262730;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
    }
    .stMetric {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🛡️ Enterprise Risk & Financial Performance Intelligence")
st.markdown("### Financial Data Analyst Mode")

# --- Sidebar ---
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL").upper()
period = st.sidebar.selectbox("Period", options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3)
interval = st.sidebar.selectbox("Interval", options=["1d", "1wk", "1mo"], index=0)

if st.sidebar.button("Analyze"):
    with st.spinner(f"Fetching data for {ticker}..."):
        # Fetch Data
        df = DataLoader.fetch_stock_data(ticker, period, interval)
        info = DataLoader.fetch_company_info(ticker)

        if df.empty:
            st.error(f"Could not fetch data for {ticker}. Please check the symbol.")
        else:
            # Calculate Metrics
            daily_returns = PerformanceAnalyzer.calculate_daily_returns(df)

            volatility = RiskAnalyzer.calculate_volatility(daily_returns)
            max_dd = RiskAnalyzer.calculate_max_drawdown(df)
            var_95 = RiskAnalyzer.calculate_historical_var(daily_returns)

            sharpe = PerformanceAnalyzer.calculate_sharpe_ratio(df)
            cagr = PerformanceAnalyzer.calculate_cagr(df)

            current_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            price_change = current_price - prev_price
            pct_change = (price_change / prev_price) * 100

            # --- Persist data in session state ---
            st.session_state["analysis_results"] = {
                "returns": daily_returns.tolist(),
                "volatility": volatility,
                "max_drawdown": max_dd,
                "value_at_risk": var_95,
                "sharpe_ratio": sharpe,
                "cagr": cagr,
                "current_price": current_price,
                "pct_change": pct_change,
            }
            st.session_state["company_metadata"] = info
            st.session_state["analysis_done"] = True

            st.success("Analysis complete! Now you can proceed to other tabs.")

# --- Tabs ---
tabs = ["Market Overview", "Risk Analysis", "Monte Carlo Simulation", "Company Info"]
selected_tab = st.selectbox("Select a Tab:", tabs)

# --- Handle Monte Carlo Simulation Tab ---
if selected_tab == "Monte Carlo Simulation":
    if not st.session_state.get("analysis_done", False):
        st.info("Please complete the analysis step first.")
    else:
        simulation_results = MonteCarloSimulator.run(
            st.session_state["analysis_results"]
        )
        st.write("## Monte Carlo Simulation Results:")
        st.write(simulation_results)

# --- Handle Company Info Tab ---
if selected_tab == "Company Info":
    company_info = st.session_state.get("company_metadata", {})

    if not company_info:
        st.info("No company metadata available. Please perform the analysis step first.")
    else:
        st.write("### Company Information")
        st.write(f"**Name:** {company_info.get('name', 'N/A')}")
        st.write(f"**Sector:** {company_info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {company_info.get('industry', 'N/A')}")