import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Download data
df = yf.download("BTC-USD", start="2023-01-01", end="2023-12-31")
df = df[['Close']]

# Step 2: Daily Return
df['Daily Return'] = df['Close'].pct_change()

# Step 3: RSI (14-day)
delta = df['Close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
df['RSI'] = 100 - (100 / (1 + rs))

# Step 4: Bollinger Bands (20-day)
df['SMA20'] = df['Close'].rolling(window=20).mean()
df['STD20'] = df['Close'].rolling(window=20).std()
df['Upper Band'] = df['SMA20'] + 2 * df['STD20']
df['Lower Band'] = df['SMA20'] - 2 * df['STD20']

# Step 5: Sharpe Ratio
risk_free_rate = 0.04
trading_days = 252
excess_return = df['Daily Return'].mean() * trading_days - risk_free_rate
volatility = df['Daily Return'].std() * (trading_days ** 0.5)
sharpe_ratio = excess_return / volatility

print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# Step 6: Plot Bollinger Bands
plt.figure(figsize=(12,6))
plt.plot(df['Close'], label='Close Price')
plt.plot(df['SMA20'], label='20-Day SMA', color='orange')
plt.plot(df['Upper Band'], label='Upper Band', linestyle='--', color='green')
plt.plot(df['Lower Band'], label='Lower Band', linestyle='--', color='red')
plt.title('BTC Price with Bollinger Bands')
plt.legend()
plt.show()
