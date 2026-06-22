
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Pro Finance Terminal", layout="wide", page_icon="⚡")

# Custom Branding CSS
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Pro-Grade Market Intelligence Engine")
st.caption("Engineered with WebSocket Simulation | NSE & BSE Latency Optimized")

# 2. Sidebar - Advanced Controls
st.sidebar.header("🕹️ Engine Controls")
symbol = st.sidebar.text_input("Asset Ticker", value="RELIANCE.NS")

# --- NEW: MODE SELECTOR ---
mode = st.sidebar.radio("Select Operational Mode", ("Historical Analysis", "Live WebSocket Feed"))

if mode == "Historical Analysis":
    # Re-introducing the timeframe options
    period = st.sidebar.selectbox("Analysis Timeframe", ("1d", "5d", "1mo", "6mo", "1y", "5y", "max"))
    st.sidebar.info("Analyze long-term trends and historical patterns.")
else:
    # Live engine settings
    refresh_rate = st.sidebar.slider("Engine Latency (ms)", 200, 2000, 500)
    st.sidebar.warning("Live Mode: High-frequency data polling active.")

# 3. Main Logic
try:
    ticker = yf.Ticker(symbol)
    
    if mode == "Historical Analysis":
        # --- HISTORICAL MODE ---
        df = ticker.history(period=period)
        
        # Display Static Metrics
        c1, c2, c3 = st.columns(3)
        current_price = df['Close'].iloc[-1]
        open_price = df['Open'].iloc[0]
        change = current_price - open_price
        
        c1.metric("Ticker", symbol)
        c2.metric("Market Price", f"₹{current_price:,.2f}" if ".NS" in symbol.upper() else f"${current_price:,.2f}", f"{change:,.2f}")
        c3.metric("Timeframe", period.upper())

        # Professional Trend Chart
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(title=f"{symbol} Historical Candlestick Chart", template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Show Data Log"):
            st.dataframe(df.tail(50), use_container_width=True)

    else:
        # --- LIVE WEBSOCKET MODE ---
        # Persistent state for the live chart
        if "live_prices" not in st.session_state:
            st.session_state.live_prices = []
            st.session_state.live_times = []

        placeholder = st.empty()

        while True:
            live_df = ticker.history(period="1d", interval="1m")
            if not live_df.empty:
                current_val = live_df['Close'].iloc[-1]
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-4]
                
                st.session_state.live_prices.append(current_val)
                st.session_state.live_times.append(timestamp)
                
                # Keep last 15 ticks for speed
                if len(st.session_state.live_prices) > 15:
                    st.session_state.live_prices.pop(0)
                    st.session_state.live_times.pop(0)

                with placeholder.container():
                    st.subheader(f"🔴 Live Streaming: {symbol}")
                    
                    # Moving Line Chart
                    live_fig = go.Figure()
                    live_fig.add_trace(go.Scatter(x=st.session_state.live_times, y=st.session_state.live_prices, mode='lines+markers', line=dict(color='#00ff41', width=4)))
                    live_fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0))
                    st.plotly_chart(live_fig, use_container_width=True)
                    
                    st.success(f"Packet Received: {timestamp} | Latency: {refresh_rate}ms")
            
            time.sleep(refresh_rate / 1000)

except Exception as e:
    st.error(f"Engine Warning: Ensure ticker '{symbol}' is valid. Error: {e}")




# --- AI STOCK/EXPENSE PREDICTION SECTION ---
st.divider()
st.subheader("🤖 AI Price/Expense Forecasting")

if st.button("Predict Next Month's Value"):
    if len(df) < 5: # Stocks need a bit more data for a trend
        st.error("Not enough data! Please ensure you have at least 5 rows of history.")
    else:
        try:
            # 1. Prepare Data
            temp_df = df.copy()
            
            # If 'Date' is hidden in the index (common in yfinance), move it to a column
            if 'Date' not in temp_df.columns:
                temp_df = temp_df.reset_index()
            
            # Standardize column names to Capitalized
            temp_df.columns = [str(c).capitalize() for c in temp_df.columns]
            
            # 2. Identify target column (Use 'Close' for stocks or 'Amount' for expenses)
            target_col = None
            for col in ['Close', 'Amount', 'Value']:
                if col in temp_df.columns:
                    target_col = col
                    break
            
            if 'Date' not in temp_df.columns or target_col is None:
                st.error(f"Missing required columns. Found: {list(temp_df.columns)}")
            else:
                # 3. Process Dates for AI
                temp_df['Date'] = pd.to_datetime(temp_df['Date'])
                # Group by date to handle duplicates, then get monthly average/sum
                monthly_df = temp_df.groupby(temp_df['Date'].dt.to_period('M'))[target_col].mean().reset_index()
                monthly_df['Month_Number'] = np.arange(len(monthly_df)) + 1

                # 4. Train AI Model
                X = monthly_df[['Month_Number']]
                y = monthly_df[target_col]
                model = LinearRegression()
                model.fit(X, y)

                # 5. Predict Next Month
                next_month_num = monthly_df['Month_Number'].max() + 1
                prediction = model.predict([[next_month_num]])

                # 6. Show Result
                st.success(f"### Predicted {target_col} for next month: **{prediction[0]:,.2f}**")
                st.info(f"AI Trend Analysis: Based on your '{target_col}' history, the model projects this future value.")
            
        except Exception as e:
            st.error(f"Error calculating prediction: {e}")



st.markdown("---")
st.markdown("Built by **Ritish S** | [GitHub](https://github.com/ritish-5a/live-finance-tracker) | 1st Year AIML")


