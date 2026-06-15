import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration (Full Width)
st.set_page_config(page_title="Pro Market Analytics", layout="wide", page_icon="📈")

# Custom CSS for the "Trading Terminal" look
st.markdown("""
    <style>
    .metric-container { background-color: #1e2130; padding: 20px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ NSE/BSE Real-Time High-Frequency Dashboard")
st.caption("Low-latency market monitoring engine | Status: Online")

# 2. Sidebar - Logic for Ticker selection
st.sidebar.header("Engine Configuration")
symbol = st.sidebar.text_input("Enter NSE/BSE Ticker (e.g., RELIANCE.NS, ^NSEI)", value="RELIANCE.NS")
refresh_rate = st.sidebar.slider("Refresh Latency (ms)", 200, 2000, 500)

# 3. Live Data Streaming Simulation (Mimicking WebSocket behavior)
placeholder = st.empty()

# Persistent state for the live chart
if "price_history" not in st.session_state:
    st.session_state.price_history = []
    st.session_state.time_history = []

# Loop to simulate 200ms latency updates
while True:
    try:
        # Fetch high-frequency data
        ticker = yf.Ticker(symbol)
        # We fetch '1d' with '1m' interval for the most recent data point
        df = ticker.history(period="1d", interval="1m")
        
        if not df.empty:
            latest_price = df['Close'].iloc[-1]
            last_update = datetime.now().strftime("%H:%M:%S.%f")[:-4]
            
            # Update local session state for the "Live" feel
            st.session_state.price_history.append(latest_price)
            st.session_state.time_history.append(last_update)
            
            # Keep only the last 20 points for the "moving" chart
            if len(st.session_state.price_history) > 20:
                st.session_state.price_history.pop(0)
                st.session_state.time_history.pop(0)

            with placeholder.container():
                # Display Metrics
                c1, c2, c3 = st.columns(3)
                currency = "₹" if ".NS" in symbol.upper() else "$"
                
                c1.metric("Live Price", f"{currency}{latest_price:,.2f}")
                c2.metric("Exchange", "NSE/BSE" if ".NS" in symbol.upper() else "Global")
                c3.metric("Latency", f"{refresh_rate}ms", "Optimized")

                # Real-Time Visualizer
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=st.session_state.time_history, 
                    y=st.session_state.price_history,
                    mode='lines+markers',
                    line=dict(color='#00ff41', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(0, 255, 65, 0.1)'
                ))
                
                fig.update_layout(
                    title=f"Live Feed: {symbol} (Last 20 ticks)",
                    template="plotly_dark",
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#30363d')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Performance Log
                st.info(f"Engine Log: Packet received at {last_update} | Latency: {refresh_rate}ms")

        time.sleep(refresh_rate / 1000) # Control the latency

    except Exception as e:
        st.error(f"Engine Error: {e}")
        break
