import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

symbols_input = input("Enter stocks to compare: ")
symbols = [symbols.strip().upper() for symbols in symbols_input.split(",")]
period = input("Enter Period: (1mo, 3mo, 6mo, 1y, 5y, max) ").lower()


print("=" * 40)
print("             STOCK COMPARER")
print("=" * 40)

print("Stocks:", symbols)

stock_data = {}
normalized_data = {}
drawdown_data = {}

results = {}

for symbol in symbols:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period)
    stock_data[symbol] = data

for symbol, data in stock_data.items():
    closing_prices = data["Close"].dropna()
    starting_price = closing_prices.iloc[0]
    ending_price = closing_prices.iloc[-1]

    normalized_price = (closing_prices / closing_prices.iloc[0]) * 100
    normalized_data[symbol] = normalized_price

    running_peak = closing_prices.cummax()
    drawdown = (closing_prices - running_peak) / running_peak
    drawdown_data[symbol] = drawdown

    daily_returns = closing_prices.pct_change()
    volatility = daily_returns.std()

    average_daily_return = daily_returns.mean()
    annualized_sharpe = (average_daily_return / volatility) * (252 ** 0.5)

    total_return = (ending_price / starting_price) - 1
    print(f"{symbol}: {total_return * 100:.2f}%")

    results[symbol] = {
        "Return": total_return,
        "Volatility": volatility,
        "Max Drawdown": drawdown.min(),
        "Sharpe": annualized_sharpe
    }

results_df = pd.DataFrame(results).T
print(results_df.to_string())

plt.figure(figsize=(7, 5))
for symbol, prices in stock_data.items():
    plt.plot(prices["Close"], label=symbol)

plt.title("Stock Prices")
plt.xlabel("Date")
plt.ylabel("Price ($USD)")
plt.legend()
plt.tight_layout
plt.show()

plt.figure(figsize=(7, 5))
for symbol, prices in normalized_data.items():
    plt.plot(prices, label=symbol)

plt.title("Normalized Stock Performance")
plt.xlabel("Date")
plt.ylabel("Value of $100 Investment")
plt.legend()
plt.tight_layout
plt.show()

plt.figure(figsize=(7, 5))
for symbol, drawdown in drawdown_data.items():
    plt.plot(drawdown * 100, label=symbol)

plt.title("Stock Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")
plt.legend()
plt.tight_layout
plt.show()