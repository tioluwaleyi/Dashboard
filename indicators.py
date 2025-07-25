import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Load data
data = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
close = data['Close']

# Bollinger Bands
window = 20
sma = close.rolling(window=window).mean()
std = close.rolling(window=window).std()

upper_band = sma + (2 * std)
lower_band = sma - (2 * std)

# Plot
plt.figure(figsize=(12,6))
plt.plot(close, label='Close Price')
plt.plot(sma, label='SMA 20', color='orange')
plt.plot(upper_band, label='Upper Band', linestyle='--', color='green')
plt.plot(lower_band, label='Lower Band', linestyle='--', color='red')
plt.fill_between(close.index, lower_band, upper_band, color='lightgray')
plt.legend()
plt.title("Bollinger Bands")
plt.show()
