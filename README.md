# UAS PPL – Monitoring & Otomatisasi IoT Berbasis MQTT

## Overview
Repositori ini berisi **sistem monitoring dan otomatisasi IoT** berbasis **ESP32** yang disimulasikan menggunakan **Wokwi**, dengan komunikasi data menggunakan **MQTT** serta **notifikasi otomatis melalui Telegram**.

Project ini bertujuan untuk menerapkan dan memahami konsep:
- Internet of Things (IoT)
- Protokol komunikasi MQTT
- Otomatisasi berbasis event
- Logging dan monitoring data sensor
- Integrasi Python dengan layanan eksternal (Telegram API)

---

## Arsitektur Sistem
```text
ESP32 + Sensor
(DHT, PIR, RTC)
       |
       | publish (MQTT)
       v
Broker MQTT (HiveMQ)
       |
       | subscribe
       v
Python Automation Script
       |
       |-- Analisis kondisi
       |-- Penyimpanan data (CSV)
       |-- Notifikasi Telegram
```

---

## Simulasi IoT
Sebagai sistem utama untuk diotomatisasi, Pakai template [Wokwi](https://wokwi.com/projects/454270041562834945) ini
```text
Komponen utama:
- ESP32
- Sensor DHT (Suhu & Kelembaban)
- PIR Sensor
- Relay (Lampu)
- RTC
- LCD I2C
```

---

## Setup Bot Telegram
Untuk menerima notifikasi otomatis, silakan membuat bot Telegram melalui **@BotFather**.

### Langkah Konfigurasi
1. Buat file bernama **`bot-tele.txt`**
2. Isi dengan format berikut:
```text
BOT_TOKEN=xxxxx:xxxxxxxxxxxxxxxxxxxx
CHAT_ID=xxxxxxxxx
```

---

## Cara Kerja Sistem
1. ESP32 membaca data dari sensor, meliputi suhu, kelembaban, dan status lampu.
2. Data dikirim ke broker MQTT dalam format **JSON**.
3. Script Python melakukan proses berikut:
   - Subscribe ke topik MQTT
   - Parsing data yang diterima
   - Analisis kondisi berdasarkan data sensor
   - Penyimpanan data ke file CSV
4. Jika sistem mendeteksi kondisi **BAHAYA**, maka:
   - Menampilkan peringatan pada terminal
   - Mengirim notifikasi otomatis ke Telegram

---

## Struktur Project
```text
ppl-uas-monitoring-iot/
│── .gitignore             	    # Ignore file sensitif
│── automation.py          	    # Script utama Python
│── bot-tele.txt           	    # Token Telegram (LOCAL ONLY)
│── laporan_otomatisasi.csv     # Log data otomatis (generated)
│── README.md              	    # Dokumentasi
│── requirements.txt       	    # Library Python
```

---

## Library yang Digunakan
External Library
- `paho-mqtt` – komunikasi MQTT
- `requests` – integrasi Telegram API
Install dependency:
```bash
pip install -r requirements.txt
```
Built-in Python
- `json`
- `csv`
- `time`
- `datetime`

---

## Output Sistem
- Real-time monitoring melalui terminal
- Logging otomatis ke file CSV
- Notifikasi Telegram saat kondisi bahaya
- Sistem berjalan event-driven

---

© 2026
UAS PPL – Monitoring IoT & Automation System
