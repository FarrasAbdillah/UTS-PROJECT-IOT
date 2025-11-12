import paho.mqtt.client as mqtt
import mysql.connector
import json
import time

# --- Pengaturan MQTT ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "farras/sensor" # Topik yang kita dengarkan

# --- Pengaturan Database ---
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'uts_pem_iot'
}

# Fungsi on_connect (Tetap Sama)
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Berhasil terhubung ke Broker MQTT! (Code: {rc})")
        client.subscribe(MQTT_TOPIC)
        print(f"Berhasil subscribe ke topik: {MQTT_TOPIC}")
    else:
        print(f"Gagal terhubung ke Broker MQTT, Code: {rc}")

# Fungsi on_message (DI-UPDATE)
def on_message(client, userdata, msg):
    print(f"Pesan diterima! Topik: {msg.topic}, Payload: {msg.payload.decode('utf-8')}")
    
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        
        # (BARU) Ambil data 'lux' dari JSON
        suhu = data.get('suhu')
        humidity = data.get('humid')
        lux = data.get('lux') # <-- INI YANG BARU

        # (BARU) Cek apakah 'lux' juga ada
        if suhu is not None and humidity is not None and lux is not None:
            # (BARU) Kirim 'lux' ke fungsi database
            insert_to_db(suhu, humidity, lux)
        else:
            print("Data JSON tidak lengkap (tidak ada 'suhu', 'humid', atau 'lux').")
            
    except json.JSONDecodeError:
        print("Gagal men-decode JSON. Pesan bukan format JSON.")
    except Exception as e:
        print(f"Terjadi error saat proses pesan: {e}")

# Fungsi insert_to_db (DI-UPDATE)
def insert_to_db(suhu, humidity, lux): # (BARU) Terima parameter 'lux'
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # (BARU) Perintah SQL sekarang menggunakan 'lux' yang asli
        sql = "INSERT INTO data_sensor (suhu, humidity, lux) VALUES (%s, %s, %s)"
        val = (suhu, humidity, lux) # <-- BUKAN LAGI 0
        
        cursor.execute(sql, val)
        conn.commit()
        
        # (BARU) Log update
        print(f">>> DATABASE UPDATE: Berhasil memasukkan data: Suhu={suhu}, Humid={humidity}, Lux={lux}")
        
    except mysql.connector.Error as err:
        print(f"Gagal memasukkan data ke DB: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# --- Program Utama (Tetap Sama) ---
def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    print("Mencoba terhubung ke MQTT Broker...")
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Tidak bisa terhubung ke broker: {e}")
        print("Cek koneksi internet atau alamat broker.")
        return

    try:
        print("Listener berjalan. Menunggu data dari Wokwi...")
        print("Tekan Ctrl+C untuk berhenti.")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nListener dihentikan.")
        client.disconnect()

if __name__ == '__main__':
    main()