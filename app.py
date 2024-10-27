from flask import Flask, render_template, request
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
            # Extract the most recent stock price
            latest_time = list(data["Time Series (1min)"])[0]
            latest_price = data["Time Series (1min)"][latest_time]["1. open"]
            return float(latest_price)
        else:
            # Handle errors in the response
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        amount = float(request.form.get("amount"))  # Convert to float for decimal input

        # Get the live price of the stock
        price = get_stock_price(symbol)
        
        if price is not None:
            # Calculate total value based on the price and amount
            total_value = price * amount
            # Add stock data to the portfolio list
            portfolio.append({
                "symbol": symbol,
                "amount": amount,
                "price": price,
                "total_value": total_value
            })
        else:
            # If there's an issue getting the price, add with "N/A" fields
            portfolio.append({
                "symbol": symbol,
                "amount": amount,
                "price": "N/A",
                "total_value": "N/A"
            })

    return render_template("index.html", portfolio=portfolio)

if __name__ == "__main__":
    app.run(debug=True)