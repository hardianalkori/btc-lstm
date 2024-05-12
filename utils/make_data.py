from utils.get_data import get_fng, get_btc_data
import joblib

high_scaler = joblib.load("model/high_scaler.joblib")
low_scaler = joblib.load("model/low_scaler.joblib")
close_scaler = joblib.load("model/close_scaler.joblib")
index_scaler = joblib.load("model/index_scaler.joblib")


def preprocessing():
	btc_data = get_btc_data()
	values, classification = get_fng()
	
	print(btc_data)
	btc_data["index"] = values
	btc_data["klasifikasi"] = classification
	btc_data = btc_data[["Date","High","Low","Close","index","klasifikasi"]]

	btc_data["high_scaled"] = high_scaler.transform(btc_data["High"].values.reshape(-1,1))
	btc_data["low_scaled"] = low_scaler.transform(btc_data["Low"].values.reshape(-1,1))
	btc_data["close_scaled"] = close_scaler.transform(btc_data["Close"].values.reshape(-1,1))
	btc_data["index_scaled"] = index_scaler.transform(btc_data["index"].values.reshape(-1,1))


	btc_data.to_excel("dataset/btc_data_new.xlsx", index = False)

	return btc_data
