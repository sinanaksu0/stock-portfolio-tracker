from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Placeholder for portfolio data
portfolio = []

# Alpha Vantage API key
API_KEY = "TKC1ADZOYQOQ7SO2"

# Function to get stock price from Alpha Vantage API
def get_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()

        # Check if we received valid data
        if "Time Series (1min)" in data:
            latest_time = list(data["Time Series (1min)"])[0]
            latest_price = data["Time Series (1min)"][latest_time]["1. open"]
            return float(latest_price)
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to search for stock symbols
def search_stock(query):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Return top 5 results if any are found
    return data.get("bestMatches", [])[:5]

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
            return render_template("index.html", portfolio=portfolio, error=error_message)

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
            return render_template("index.html", portfolio=portfolio, error=error_message)

    return render_template("index.html", portfolio=portfolio)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    results = search_stock(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)