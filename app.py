from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

# Placeholder for portfolio data
portfolio = []

# Function to get stock price from yfinance
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        return float(hist['Open'][0])
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        try:
            amount = float(request.form.get("amount"))
        except ValueError:
            amount = -1

        # Validate positive amount and valid stock symbol
        if amount < 0:
            error_message = "Please enter a positive amount."
            return render_template("index.html", portfolio=portfolio, error=error_message, total_portfolio_value=calculate_total_portfolio_value())

        price = get_stock_price(symbol)
        if price is not None:
            total_value = price * amount
            portfolio.append({
                "symbol": symbol,
                "amount": amount,
                "price": price,
                "total_value": total_value
            })
        else:
            error_message = "Invalid stock symbol."
            return render_template("index.html", portfolio=portfolio, error=error_message, total_portfolio_value=calculate_total_portfolio_value())

    return render_template("index.html", portfolio=portfolio, total_portfolio_value=calculate_total_portfolio_value())

# Function to calculate total portfolio value
def calculate_total_portfolio_value():
    return sum(stock['total_value'] for stock in portfolio)

if __name__ == "__main__":
    app.run(debug=True)