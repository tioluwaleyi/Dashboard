import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial + Technical Dashboard", layout="wide")
st.title("📊 ChainSight: Financial & Technical Indicator Dashboard")

# Sidebar controls
st.sidebar.header("Select Options")
asset = st.sidebar.text_input("Asset Ticker (e.g. BTC-USD, AAPL)", value="BTC-USD")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))

# Load data
@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    df = df[['Close']]
    df['Daily Return'] = df['Close'].pct_change()
    return df

df = load_data(asset, start_date, end_date)

# Technical Indicators
delta = df['Close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss
df['RSI'] = 100 - (100 / (1 + rs))

df['SMA20'] = df['Close'].rolling(20).mean()
df['Upper Band'] = df['SMA20'] + 2 * df['Close'].rolling(20).std()
df['Lower Band'] = df['SMA20'] - 2 * df['Close'].rolling(20).std()

# Sharpe Ratio
risk_free_rate = 0.04
trading_days = 252
excess_return = df['Daily Return'].mean() * trading_days - risk_free_rate
volatility = df['Daily Return'].std() * np.sqrt(trading_days)
sharpe_ratio = excess_return / volatility

# Display metrics
st.subheader(f"{asset} Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Annual Return", f"{(df['Daily Return'].mean() * trading_days):.2%}")
col2.metric("Volatility", f"{volatility:.2%}")
col3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

# Price Chart with Bollinger Bands
st.subheader("Price Chart with Bollinger Bands")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df['Close'], label="Close", color='blue')
ax.plot(df['SMA20'], label="SMA 20", color='orange')
ax.fill_between(df.index, df['Upper Band'], df['Lower Band'], color='gray', alpha=0.3)
ax.legend()
st.pyplot(fig)

# RSI Chart
st.subheader("RSI (14-day)")
fig2, ax2 = plt.subplots(figsize=(12, 2))
ax2.plot(df['RSI'], color='purple')
ax2.axhline(70, color='red', linestyle='--')
ax2.axhline(30, color='green', linestyle='--')
ax2.set_ylim(0, 100)
st.pyplot(fig2)
