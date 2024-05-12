from keras.models import load_model
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import joblib
import pandas as pd
import yfinance
import pytz

import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(
    page_title = "Dashboard Forecasting", layout = "wide")

st.markdown("<h1 style='text-align: center; color: white;'>Dashboard Forecasting</h1>", unsafe_allow_html=True)

today_date = datetime.today().date()

tickers = yf.Tickers('btc-usd')
today = tickers.tickers['BTC-USD'].history(period="1d", interval="1h")
utc_now = datetime.now(pytz.utc).date()
high_today =  max(today["High"])
low_today = min(today["Low"])

high_scaler = joblib.load("model/high_scaler.joblib")
low_scaler = joblib.load("model/low_scaler.joblib")
close_scaler = joblib.load("model/close_scaler.joblib")
index_scaler = joblib.load("model/index_scaler.joblib")

model = load_model("model/BTC-128-256-3L-350EPOCH.h5", compile = False)

df = pd.read_excel("dataset/btc_data_new.xlsx")
history_forecast = pd.read_excel("dataset/history_forecast.xlsx")[["date","high","low","close"]]
x_last = df[["index","high_scaled", "low_scaled", "close_scaled"]][1:-1].values.reshape(-1,30,4)

with st.sidebar:
	st.subheader("Harga Saat Ini: "+str(today["Close"].iloc[-1]))
	st.write("High:",high_today, "Low:",low_today )

col1, col2 = st.columns(2)

def inverse(high, low, close):
	high_scaled = high_scaler.inverse_transform([[high]])
	low_scaled = low_scaler.inverse_transform([[low]])
	close_scaled = close_scaler.inverse_transform([[close]])
	
	return high_scaled[0][0], low_scaled[0][0], close_scaled[0][0]

def forecast():
    pred = model.predict(x_last)
    next_high, next_low, next_close = inverse(pred[0][0], pred[0][1], pred[0][2])
    current_error_high = ((next_high - high_today) / high_today) * 100
    current_error_low = abs((next_low - low_today) / low_today) * 100

    with col2:
    	st.subheader("Data Histori Forecast")
    	st.dataframe(history_forecast, width=450, height=350)
    	

	
    chart(next_high, next_low, next_close)
    save_forecast(next_high, next_low, next_close)

def chart(next_high, next_low, next_close):
	plt.style.use('dark_background')
	plt.figure(figsize=(10, 6))
	plt.plot(today.index, today["Close"], label='Harga Bitcoin')
	plt.axhline(next_high, color='g', linestyle='-', label='Prediksi High Hari Ini')
	plt.axhline(next_low, color='r', linestyle='-', label='Prediksi Low Hari Ini')
	plt.axhline(next_close, color='y', linestyle='-', label='Prediksi Close Hari Ini')
	plt.xlabel('Tanggal')
	plt.ylabel('Harga BTC (USD)')
	plt.legend(loc = "lower left")
	with col1:
		st.subheader('Grafik Forecast '+str(utc_now) + " UTC")
		st.write("H:", next_high, "L:", next_low, "Close:", next_close)
		st.pyplot(plt)

def save_forecast(next_high, next_low, next_close):
	data_forecast = pd.read_excel("dataset/history_forecast.xlsx")
	data_forecast["date"] = data_forecast["date"]
	if utc_now not in data_forecast["date"].tolist():
		data_forecast.loc[len(data_forecast)] = {"date":utc_now, "high":next_high, "low":next_low, "close":next_close}
		data_forecast.to_excel("dataset/history_forecast.xlsx", index = False)

forecast()
st.subheader("Data Histori Harga Bitcoin Hari Ini")
st.dataframe(today[["Open", "High", "Low","Close", "Volume"]].sort_values(by="Datetime"), width = 980, height = 900)

