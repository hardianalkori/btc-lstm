import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
import sys
import streamviz

from utils.updater_metrics import updater

st.set_page_config(
    page_title = "Dashboard Performa", layout = "wide")

st.markdown("<h1 style='text-align: center; color: white;'>Dashboard Performa</h1>", unsafe_allow_html=True)
st.subheader("Grafik Perbedaan Aktual VS Prediksi")
data_histori = pd.read_excel("dataset/history_forecast.xlsx")
data_histori = data_histori[:-1]
data_histori.set_index("date", inplace=True)
data_histori.index = data_histori.index.date

data_metrik = pd.read_excel("dataset/metrics_data.xlsx")
data_metrik["date"] = data_metrik["date"].dt.date
mape_overall = (data_metrik["ape_high"].mean() + data_metrik["ape_low"].mean() + data_metrik["ape_low"].mean()) / 3

updater(data_histori)

col1, col2 = st.columns(2)
colheader, colheader2 = st.columns(2)
col1g, col2g, col3g = st.columns(3)


def chart_high():
    plt.figure(figsize = (10,6))
    plt.plot(data_metrik["date"], data_metrik["true_high"], label = "High Aktual")
    plt.plot(data_metrik["date"], data_metrik["high"], label = "High Prediksi")
    plt.title("High", size=20)
    plt.xlabel("Tanggal")
    plt.ylabel("Harga")
    plt.legend()

    return st.pyplot(plt)

def chart_low():
    plt.figure(figsize = (10,6))
    plt.plot(data_metrik["date"], data_metrik["true_low"], label = "Low Aktual")
    plt.plot(data_metrik["date"], data_metrik["low"], label = "Low Prediksi")
    plt.title("Low", size=20)
    plt.xlabel("Tanggal")
    plt.ylabel("Harga")
    plt.legend()

    return st.pyplot(plt)

def chart_close():
    plt.figure(figsize = (10,6))
    plt.plot(data_metrik["date"], data_metrik["true_close"], label = "Close Aktual")
    plt.plot(data_metrik["date"], data_metrik["close"], label = "Close Prediksi")
    plt.title("Close", size=20)
    plt.xlabel("Tanggal")
    plt.ylabel("Harga")
    plt.legend()

    return st.pyplot(plt)

def plot_chart():
    with col1:
        chart_high()
        chart_close()
    with col2:
        chart_low()
        st.subheader("Rata-Rata Persentase Error")#
        st.write("Berdasarkan Persentase Error Terdahulu Hingga Kemarin")
        st.markdown(CreateProgressBar("HIGH", round(data_metrik["ape_high"].mean()*100,2), "#A5D6A7", "#B2EBF2"), True)
        st.markdown(CreateProgressBar("LOW", round(data_metrik["ape_low"].mean()*100, 2), "#FFD54F", "#B2EBF2"), True)
        st.markdown(CreateProgressBar("CLOSE", round(data_metrik["ape_close"].mean()*100, 2), "red", "#B2EBF2"), True)

def CreateProgressBar(pg_caption, pg_float_percentage, pg_colour, pg_bgcolour):
    pg_int_percentage = pg_float_percentage

    if pg_int_percentage >= 3:
        pg_colour = f"rgb(255, {int(2.55 * pg_int_percentage)}, 0)" 
    elif pg_int_percentage >= 2:
        pg_colour = "orange"
    else:
        pg_colour = f"rgb({255 - int(2.55 * (pg_int_percentage - 50))}, 255, 0)"
 # Hijau ke Merah
    pg_html = f"""<table style="width:100%; border-style: none;">
                        <tr style='font-weight:bold;'>
                            <td style='background-color: transparent;'>{pg_caption}: <span style='accent-color: {pg_colour}; bgcolor: transparent;'>
                                <progress value='{pg_float_percentage}' max='5'>{pg_int_percentage}%</progress> </span>{pg_int_percentage}% 
                            </td>
                        </tr>
                    </table><br>"""
    return pg_html

 

with st.sidebar:
	streamviz.gauge(mape_overall, sFix="%", gSize="LRG", gTitle="MAPE Keseluruhan (H, L, C)", gTheme="White", gcLow = "#1B8720", gcHigh = "#FF1708", grLow = 0.015, grMid = 0.025)



plot_chart()
colheader.subheader("Histori Selisih Dan Persentase Error")
st.dataframe(data_metrik, width=1500 , height = 400)