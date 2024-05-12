
# BTC LSTM

Dashboard Harga, Peramalan Harga Bitcoin menggunakan model LSTM (Long Short Term Memory) dan Dashboard Performa Prediksi.

# Fitur
## Dashboard Utama
![App Screenshot](https://raw.githubusercontent.com/hardianalkori/btc-lstm/main/screenshot/home.png)

## Peramalan
![App Screenshot](https://raw.githubusercontent.com/hardianalkori/btc-lstm/main/screenshot/forecast.png)

## Dashboard Performa
![App Screenshot](https://raw.githubusercontent.com/hardianalkori/btc-lstm/main/screenshot/performa.png)

# Instalasi

Clone repository ini

```bash
  git clone https://github.com/hardianalkori/btc-lstm.git
  cd btc-lstm
```
Install library yang diperlukan
```bash
  pip install -r requirements.txt
```
Jalankan
```bash
  streamlit run "Halaman Utama.py"
```
    

# Catatan Penting

- Butuh Koneksi Internet
-  Model di desain memprediksi 1 langkah kedepan (Hari ini)
-  Model ini menggunakan input window size 30 hari kebelakang untuk memprediksi 1 langkah kedepan (Hari ini).
- Dikarenakan menggunakan 30 hari kebelakang, salah satu kelemahan aplikasi ini adalah hanya dapat digunakan pada jam 13:30 WIB atau 06:30AM UTC dikarenakan aplikasi ini menggunakan library yfinance yang dimana data di update pada jam tersebut.
