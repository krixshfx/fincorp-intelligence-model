import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add current directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.data.loader import DataLoader
from app.core.performance import PerformanceAnalyzer
from app.core.risk import RiskAnalyzer
from app.core.simulation import MonteCarloSimulator

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

            # --- Dashboard Layout ---
            
            # Top Metrics Row
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Current Price", f"${current_price:,.2f}", f"{pct_change:.2f}%")
            with col2:
                st.metric("Sharpe Ratio", f"{sharpe:.2f}")
            with col3:
                st.metric("Volatility (Ann.)", f"{volatility:.2%}")
            with col4:
                st.metric("Max Drawdown", f"{max_dd:.2%}", delta_color="inverse")
            with col5:
                st.metric("VaR (95%)", f"{var_95:.2%}", delta_color="inverse")

            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Market Overview", "Risk Analysis", "Monte Carlo Simulation", "Company Info"])
            
            with tab1:
                st.subheader("Price History & Volume")
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                    vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                                    row_width=[0.2, 0.7])

                # Candlestick
                fig.add_trace(go.Candlestick(x=df['Date'],
                                open=df['Open'], high=df['High'],
                                low=df['Low'], close=df['Close'], name="OHLC"), 
                                row=1, col=1)

                # Volume
                fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name="Volume", marker_color='rgba(0,0,250,0.3)'), 
                                row=2, col=1)

                fig.update_layout(xaxis_rangeslider_visible=False, height=600, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
            with tab2:
                col_risk1, col_risk2 = st.columns(2)
                
                with col_risk1:
                    st.subheader("Return Distribution")
                    fig_hist = go.Figure(data=[go.Histogram(x=daily_returns, nbinsx=50, name="Returns")])
                    fig_hist.update_layout(title_text="Daily Returns Distribution", template="plotly_dark")
                    st.plotly_chart(fig_hist, use_container_width=True)
                    
                with col_risk2:
                    st.subheader("Drawdown Analysis")
                    # Calculate drawdown series
                    prices = df['Close']
                    rolling_max = prices.cummax()
                    drawdown = (prices - rolling_max) / rolling_max
                    
                    fig_dd = go.Figure()
                    fig_dd.add_trace(go.Scatter(x=df['Date'], y=drawdown, fill='tozeroy', name="Drawdown", line=dict(color='red')))
                    fig_dd.update_layout(title_text="Underwater Plot", template="plotly_dark")
                    st.plotly_chart(fig_dd, use_container_width=True)
            
            with tab3:
                st.subheader("Monte Carlo Simulation (Future Price Projection)")
                
                col_sim1, col_sim2 = st.columns([1, 3])
                
                with col_sim1:
                    sim_days = st.slider("Days to Forecast", 30, 365, 252)
                    num_sims = st.slider("Number of Simulations", 100, 1000, 200)
                    
                    if st.button("Run Simulation"):
                        with st.spinner("Running Monte Carlo..."):
                            # Parameters
                            mu = daily_returns.mean() * 252
                            sigma = volatility
                            start_price = current_price
                            
                            # Run Sim
                            paths = MonteCarloSimulator.simulate_future_prices(
                                start_price, mu, sigma, sim_days, num_sims
                            )
                            stats = MonteCarloSimulator.get_simulation_stats(paths)
                            
                            st.session_state['sim_paths'] = paths
                            st.session_state['sim_stats'] = stats
                            
                with col_sim2:
                    if 'sim_paths' in st.session_state:
                        paths = st.session_state['sim_paths']
                        stats = st.session_state['sim_stats']
                        
                        # Plot Paths
                        fig_sim = go.Figure()
                        # Add first 50 paths to avoid lag
                        x_axis = list(range(sim_days))
                        for i in range(min(num_sims, 50)):
                            fig_sim.add_trace(go.Scatter(x=x_axis, y=paths[:, i], mode='lines', 
                                                         line=dict(width=1, color='rgba(0, 255, 255, 0.1)'), showlegend=False))
                        
                        # Add Mean Path
                        mean_path = np.mean(paths, axis=1)
                        fig_sim.add_trace(go.Scatter(x=x_axis, y=mean_path, mode='lines', 
                                                     name="Mean Path", line=dict(color='yellow', width=2)))
                        
                        fig_sim.update_layout(title="Projected Price Paths (Geometric Brownian Motion)", 
                                              xaxis_title="Days into Future", yaxis_title="Price", template="plotly_dark")
                        st.plotly_chart(fig_sim, use_container_width=True)
                        
                        # Display Stats
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Exp. Price", f"${stats['mean_price']:,.2f}")
                        c2.metric("Worst Case (5%)", f"${stats['percentile_5']:,.2f}")
                        c3.metric("Best Case (95%)", f"${stats['percentile_95']:,.2f}")
                    else:
                        st.info("Click 'Run Simulation' to generate forecasts.")

            with tab4:
                st.subheader("Fundamental Data")
                if info:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
                        st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
                        st.markdown(f"**Market Cap:** ${info.get('marketCap', 0):,.0f}")
                        st.markdown(f"**Employees:** {info.get('fullTimeEmployees', 'N/A')}")
                    with c2:
                        st.markdown(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                        st.markdown(f"**Forward P/E:** {info.get('forwardPE', 'N/A')}")
                        st.markdown(f"**Beta:** {info.get('beta', 'N/A')}")
                        st.markdown(f"**Dividend Yield:** {info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "**Dividend Yield:** N/A")
                    
                    st.markdown("### Business Summary")
                    st.info(info.get('longBusinessSummary', 'No summary available.'))
                else:
                    st.warning("No company info available.")

else:
    st.info("👈 Enter a ticker symbol and click 'Analyze' to start.")
