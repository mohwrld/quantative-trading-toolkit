import yfinance as yf
import matplotlib.pyplot as plt

symbol = input("Enter Stock Ticker: ").upper()
ticker = yf.Ticker(symbol)
data = ticker.history(period="1y")

print("Stock:", ticker.ticker)


## print(data)

closing_prices = data["Close"]

print(f"Latest Closing Price: ${closing_prices.iloc[-1]:.2f}")
print(f"Highest Closing Price: ${closing_prices.max():.2f}")
print(f"Lowest Closing Price: ${closing_prices.min():.2f}")
print(f"Average Closing Price: ${closing_prices.mean():.2f}")

starting_price = closing_prices.iloc[0]
ending_price = closing_prices.iloc[-1]
total_return = (((ending_price / starting_price) - 1) * 100)
print(f"1 Year Return: {total_return:.2f}%")

daily_returns = closing_prices.pct_change()
## print(daily_returns * 100)

average_daily_return = daily_returns.mean()
print(f"Average Daily Return: {average_daily_return * 100:.2f}%")

volatility = daily_returns.std()
## print(f"Daily Volatility: {volatility * 100:.2f}%")

cumulative_returns = (1 + daily_returns).cumprod()
total_return = ((cumulative_returns.iloc[-1] - 1) * 100)
print(f"Total Return: {total_return:.2f}%")

running_peak = closing_prices.cummax()
drawdown = (closing_prices - running_peak) / running_peak
maximum_drawdown = drawdown.min()
print(f"Maximum Drawdown: {maximum_drawdown * 100:.2f}%")

sharpe_ratio = average_daily_return / volatility
print(f"Daily Sharpe Ratio: {sharpe_ratio:.2f}")

annualized_sharpe = (average_daily_return / volatility) * (252 ** 0.5)
print(f"Annualized Sharpe Ratio: {annualized_sharpe:.2f}")

plt.plot(closing_prices)
plt.title(f"{ticker.ticker} Closing Price")
plt.xlabel("Date")
plt.ylabel("Price ($USD)")
plt.show()

plt.plot(drawdown * 100)
plt.title(f"{ticker.ticker} Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")
plt.show()