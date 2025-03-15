from flask import Flask, render_template, request
import requests

app = Flask(__name__)

key = "adaab67a74ebbb7a449d6d5dd87142c7"


def fetch_data(symbol, timeframe):
    if timeframe == "daily":
        response = requests.get(f"http://api.marketstack.com/v1/eod?access_key={key}&symbols={symbol}")
    elif timeframe == "monthly":
        response = requests.get(
            f"http://api.marketstack.com/v1/eod?access_key={key}&symbols={symbol}&date_from=2025-02-01&date_to=2025-02-28")
    elif timeframe == "yearly":
        response = requests.get(
            f"http://api.marketstack.com/v1/eod?access_key={key}&symbols={symbol}&date_from=2024-01-01&date_to=2024-12-31")
    else:
        return None

    data = response.json()
    if "data" not in data or len(data["data"]) < 2:
        return None

    change = data["data"][-1]["close"] - data["data"][0]["open"]
    stock_data = {
        "open": data["data"][0]["open"],
        "close": data["data"][-1]["close"],
        "price_change": round(change, 2),
        "percent_change": f"{round((change / data['data'][0]['open']) * 100, 2)}%"
    }
    return stock_data


@app.route("/", methods=["GET", "POST"])
def index():
    stock_info = None
    if request.method == "POST":
        symbol = request.form["symbol"].upper()
        timeframe = request.form["timeframe"]
        stock_info = fetch_data(symbol, timeframe)
    return render_template("index.html", stock_info=stock_info)


if __name__ == "__main__":
    app.run(debug=True)
