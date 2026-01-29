import paho.mqtt.client as mqtt
import json
import csv
import time
import requests
from datetime import datetime

MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "uastekkom/data/ppl" 
CSV_FILE = "laporan-otomatisasi.csv"

with open("bot-tele.txt") as f:
    BOT_TOKEN = f.readline().strip()
    CHAT_ID = f.readline().strip()

def kirim_telegram(pesan):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": pesan}
        requests.post(url, data=data)
        print(">> Notifikasi Telegram Terkirim!")
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")

try:
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Waktu", "Suhu (°C)", "Kelembaban (%)", "Lampu", "Kondisi"])
except Exception as e:
    print(f"Error file CSV: {e}")

def on_connect(client, userdata, flags, rc):
    print(f"Terhubung ke Broker! (Kode: {rc})")
    client.subscribe(MQTT_TOPIC)
    print(f"Standby memantau topik: {MQTT_TOPIC}...")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        
        suhu = data.get('suhu', 0)
        hum = data.get('kelembaban', 0)
        lampu = data.get('lampu', 'UNKNOWN')
        kondisi = data.get('alert', 'AMAN')
        
        raw_time = data.get('waktu_rtc', 'Error')
        if raw_time == "Error" or raw_time == "No RTC":
            waktu_fix = datetime.now().strftime("%H:%M:%S") 
        else:
            waktu_fix = raw_time

        print(f"[{waktu_fix}] T:{suhu}°C | H:{hum}% | Lampu:{lampu} | Kondisi:{kondisi}")
        
        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([waktu_fix, suhu, hum, lampu, kondisi])
            
        if kondisi == "BAHAYA":
            print(">>> PERINGATAN: SUHU TERLALU PANAS! <<<")
            pesan_alert = (
                f"🚨 PERINGATAN BAHAYA!\n\n"
                f"Suhu: {suhu}°C\n"
                f"Kelembaban: {hum}%\n"
                f"Waktu: {waktu_fix}\n"
                f"Status: SUHU PANAS!"
            )
            kirim_telegram(pesan_alert)

    except Exception as e:
        print(f"Error data skip: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("=== PROGRAM PYTHON LANJUT MONITORING SIAP ===")
try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nProgram dihentikan user.")
except Exception as e:
    print(f"Gagal koneksi internet: {e}")