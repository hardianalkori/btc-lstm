import pandas as pd
import yfinance as yf
import numpy as np

def updater(df):
    for i in df.index:
        if np.isnan(df.loc[i]["true_high"]):
            bitcoin_data = yf.download('BTC-USD',str(i))
            high = bitcoin_data.loc[str(i)]["High"]
            low = bitcoin_data.loc[str(i)]["Low"]
            close = bitcoin_data.loc[str(i)]["Close"]
            df.loc[i,["true_high", "true_low", "true_close"]] = [high, low, close]
    ape(df)

def ape(df):
    df["ape_high"] = abs((df["true_high"] - df["high"]) / df["true_high"])
    df["ape_low"] = abs((df["true_low"] - df["low"]) / df["true_low"])
    df["ape_close"] = abs((df["true_close"] - df["close"]) / df["true_close"])
    save_data(df)

def save_data(df):
    df.reset_index(drop = False, inplace = True)
    df.rename(columns={'index': 'date'}, inplace=True)
    df.to_excel("dataset/metrics_data.xlsx", index = False)