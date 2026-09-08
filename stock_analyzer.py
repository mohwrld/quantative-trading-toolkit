import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import PercentFormatter

symbol = input("Enter Stock Ticker: ").upper()
period = input("Enter Period: (1mo, 3mo, 6mo, 1y, 5y, max) ").lower()

ticker = yf.Ticker(symbol)
data = ticker.history(period=period)

print("=" * 40)
print("             STOCK ANALYZER")
print("=" * 40)

print("Stock:", ticker.ticker)
print("Period:", period)

info = ticker.info
market_cap = info.get("marketCap")
trailing_pe = info.get("trailingPE")
forward_pe = info.get("forwardPE")
cash = info.get("totalCash")
total_debt = info.get("totalDebt")
debt_to_equity = info.get("debtToEquity")


print(f"Market Cap: ${market_cap:,}" if market_cap is not None else "Market Cap: N/A")

print(f"Trailing P/E: {trailing_pe:.2f}" if trailing_pe else "Trailing P/E: N/A")

print(f"Forward P/E: {forward_pe:.2f}" if forward_pe else "Forward P/E: N/A")

print(f"Cash: ${cash:,}" if cash else "Cash: N/A")

print(f"Total Debt: ${total_debt:,}" if total_debt else "Total Debt: N/A")

print(f"Debt-to-Equity: {debt_to_equity:.2f}x" if debt_to_equity else "Debt-to-Equity: N/A")

## print(data)

closing_prices = data["Close"]

print("\nPERFORMANCE")
print("-" * 40)
print(f"Latest Closing Price: ${closing_prices.iloc[-1]:.2f}")
print(f"Highest Closing Price: ${closing_prices.max():.2f}")
print(f"Lowest Closing Price: ${closing_prices.min():.2f}")
print(f"Average Closing Price: ${closing_prices.mean():.2f}")

starting_price = closing_prices.iloc[0]
ending_price = closing_prices.iloc[-1]
total_return = (((ending_price / starting_price) - 1) * 100)
print(f"{period} Return: {total_return:.2f}%")

daily_returns = closing_prices.pct_change()
## print(daily_returns * 100)

average_daily_return = daily_returns.mean()
print(f"Average Daily Return: {average_daily_return * 100:.2f}%")

win_rate = (daily_returns > 0).mean()
print(f"Win Rate: {win_rate * 100:.2f}%")

print("\nRISK")
print("-" * 40)

volatility = daily_returns.std()
print(f"Daily Volatility: {volatility * 100:.2f}%")

rolling_volatility = (daily_returns.rolling(20).std()) * (252 ** 0.5)

cumulative_returns = (1 + daily_returns).cumprod()
total_return = ((cumulative_returns.iloc[-1] - 1) * 100)
## print(f"Total Return: {total_return:.2f}%")

running_peak = closing_prices.cummax()
drawdown = (closing_prices - running_peak) / running_peak
maximum_drawdown = drawdown.min()
print(f"Maximum Drawdown: {maximum_drawdown * 100:.2f}%")

sharpe_ratio = average_daily_return / volatility
print(f"Daily Sharpe Ratio: {sharpe_ratio:.2f}")

annualized_sharpe = (average_daily_return / volatility) * (252 ** 0.5)
print(f"Annualized Sharpe Ratio: {annualized_sharpe:.2f}")

average_gain = daily_returns[daily_returns > 0].mean()
print(f"Average Gain: {average_gain:.2%}")

average_loss = daily_returns[daily_returns < 0].mean()
print(f"Average Loss: {average_loss:.2%}")



if period in ["1mo", "3mo"]:
    locator = mdates.WeekdayLocator()
    formatter = mdates.DateFormatter("%b %d")
elif period in ["6mo", "1y"]:
    locator = mdates.MonthLocator()
    formatter = mdates.DateFormatter("%b %Y")
else:
    locator = mdates.YearLocator()
    formatter = mdates.DateFormatter("%Y")

plt.figure(figsize=(7,5))
plt.plot(closing_prices)
plt.title(f"{ticker.ticker} Closing Price")
plt.xlabel("Date")
plt.ylabel("Price ($USD)")
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xticks(rotation=30)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

plt.figure(figsize=(7,5))
plt.plot(drawdown * 100)
plt.title(f"{ticker.ticker} Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xticks(rotation=30)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

average_return = daily_returns.mean()

plt.figure(figsize=(7,5))
plt.hist(daily_returns.dropna(), bins = 50)
plt.title(f"{ticker.ticker} Daily Returns Distribution")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
plt.axvline(average_return, color="black", linestyle="--", linewidth=1.0, label=f"Average: {average_return:.2%}")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(7,5))
plt.plot(rolling_volatility * 100)
plt.title(f"{ticker.ticker} 20-Day Rolling Volatility")
plt.xlabel("Date")
plt.ylabel("Annualized Volatility (%)")
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xticks(rotation=30)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()