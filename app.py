import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# 1. UI Setup
st.set_page_config(page_title="Market Tracker", layout="wide")
st.title("📈 Real-Time Market Analytics")

# 2. Sidebar for User Input
st.sidebar.header("Data Settings")
symbol = st.sidebar.text_input("Enter Ticker (e.g. AAPL, TSLA, BTC-USD)", value="BTC-USD")
period = st.sidebar.selectbox("Timeframe", ("1d", "5d", "1mo", "1y", "max"))

# 3. Data Fetching
try:
    data = yf.Ticker(symbol)
    df = data.history(period=period)
    
    # Calculate Metrics
    current_price = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[0]
    change = current_price - prev_close
    
    # 4. Display Metrics
    col1, col2 = st.columns(2)
    col1.metric("Asset", symbol.upper())
    col2.metric("Current Price", f"${current_price:,.2f}", f"{change:,.2f}")

    # 5. Create the Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], line=dict(color='#02ab21')))
    fig.update_layout(title=f"{symbol.upper()} Price Trend", template="plotly_dark")
    
    st.plotly_chart(fig, use_container_width=True)

    # 6. Show Raw Data
    st.write("### Historical Data")
    st.dataframe(df.tail(10))

except:
    st.error("Invalid Symbol. Please check the ticker (e.g., use BTC-USD for Bitcoin).")