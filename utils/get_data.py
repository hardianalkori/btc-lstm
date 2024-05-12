from urllib.request import urlopen
import json
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def get_fng():
    url = "https://api.alternative.me/fng/?limit=32&format=json&date_format=us"
    response = urlopen(url)
    data_json = json.loads(response.read())

    fng = pd.DataFrame(data_json["data"])[["value", "value_classification", "timestamp"]]
    fng["timestamp"] = pd.to_datetime(fng["timestamp"])
    fng = fng.sort_values(by="timestamp", ascending=True)

    return fng["value"].tolist(), fng["value_classification"].tolist()

def get_btc_data():
    end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=31)).strftime('%Y-%m-%d')

    btc_data = yf.download('BTC-USD', start=start_date, end=end_date)

    btc_data = btc_data.reset_index(drop=False)


    return btc_data.sort_values(by="Date")