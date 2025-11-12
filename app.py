import mysql.connector
from flask import Flask, jsonify, render_template # Tambahkan render_template

# --- Pengaturan Aplikasi Flask ---
app = Flask(__name__)

# --- Pengaturan Koneksi Database ---
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'uts_pem_iot'
}

# --- HALAMAN UTAMA: Dashboard Web ---
# Ini akan menyajikan file 'index.html'
@app.route('/')
def index_page():
    # Flask akan otomatis mencari file 'index.html'
    # di dalam folder bernama 'templates'
    return render_template('index.html')


# --- ENDPOINT API: Data Statistik ---
# Ini adalah kode lama kita, tapi di alamat baru
@app.route('/api/stats')
def get_sensor_stats():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Query Agregat (Max, Min, Avg)
        query_agg = """
        SELECT
            MAX(suhu) AS suhumax,
            MIN(suhu) AS suhumin,
            AVG(suhu) AS suhurata
        FROM data_sensor
        """
        cursor.execute(query_agg)
        data_agregat = cursor.fetchone()

        # 2. Query Detail (Sekarang jadi 10 Log Terbaru)
        query_detail = """
        SELECT
            id AS idx,
            suhu AS suhun,
            humidity AS humid,
            lux AS kecerahan,
            timestamp
        FROM data_sensor
        ORDER BY timestamp DESC  -- Mengurutkan dari yang paling BARU
        LIMIT 10                -- Hanya ambil 10 data teratas
        """
        cursor.execute(query_detail)
        data_detail_rows = cursor.fetchall()

        # 3. Proses data (termasuk month_year)
        month_year_max_list = []
        for row in data_detail_rows:
            ts = row['timestamp'] 
            month_year_str = f"{ts.month}-{ts.year}"
            month_year_max_list.append({'month_year': month_year_str})
            row['timestamp'] = ts.strftime('%Y-%m-%d %H:%M:%S')

        # 4. Susun JSON akhir
        final_json_output = {
            "suhumax": data_agregat['suhumax'],
            "suhumin": data_agregat['suhumin'],
            "suhurata": round(data_agregat['suhurata'], 2),
            "nilai_suhu_max_humid_max": data_detail_rows,
            "month_year_max": month_year_max_list
        }
        
        cursor.close()
        conn.close()
        
        # Kembalikan sebagai JSON
        return jsonify(final_json_output)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# --- Menjalankan Server Flask ---
if __name__ == '__main__':
    # Pastikan debug=True
    app.run(debug=True, port=5000)