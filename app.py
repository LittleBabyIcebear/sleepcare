from flask import Flask, request, jsonify
from google.cloud import bigquery
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Inisialisasi BigQuery client
client = bigquery.Client.from_service_account_json('C:/Database/Sleep Aja Ga Sih!/new apnea/Sleep-Apnea/Flask Model/sleepcare-428605-767355c54dde.json')

# Nama dataset dan tabel di BigQuery
dataset_id = 'my_dataset'


@app.route('/register', methods=['POST'])
def register():
    table_id = 'User' 
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Generate UUID untuk ID
    user_id = str(uuid.uuid4())
    
    # Buat query untuk menambahkan user baru
    query = f"""
    INSERT INTO `{dataset_id}.{table_id}` (ID, username, password)
    VALUES ('{user_id}', '{username}', '{password}')
    """
    
    # Eksekusi query
    query_job = client.query(query)
    query_job.result()  # Tunggu hingga query selesai
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    table_id = 'User' 
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Buat query untuk memeriksa user
    query = f"""
    SELECT * FROM `{dataset_id}.{table_id}`
    WHERE username = '{username}' AND password = '{password}'
    """
    
    # Eksekusi query
    query_job = client.query(query)
    results = query_job.result()
    
    # Cek apakah user ditemukan
    if len(list(results)) > 0:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/user_attributes', methods=['POST'])
def user_attributes():
    attributes_table_id = 'UserAttributes'
    data = request.get_json()
    user_id = data.get('user_id')
    nama = data.get('nama')
    usia = data.get('usia')
    tinggi_badan = data.get('tinggi_badan')
    berat_badan = data.get('berat_badan')
    nama_terdekat_1 = data.get('nama_terdekat_1')
    nama_terdekat_2 = data.get('nama_terdekat_2')
    nama_terdekat_3 = data.get('nama_terdekat_3')
    telepon_terdekat_1 = data.get('telepon_terdekat_1')
    telepon_terdekat_2 = data.get('telepon_terdekat_2')
    telepon_terdekat_3 = data.get('telepon_terdekat_3')
    
    # Buat query untuk menambahkan atau memperbarui atribut pengguna
    query = f"""
    MERGE `{dataset_id}.{attributes_table_id}` T
    USING (SELECT '{user_id}' AS User_ID) S
    ON T.User_ID = S.User_ID
    WHEN MATCHED THEN
      UPDATE SET Nama = '{nama}', Usia = {usia}, Tinggi_Badan = {tinggi_badan}, Berat_Badan = {berat_badan},
                 Nama_Orang_Terdekat_1 = '{nama_terdekat_1}', Nama_Orang_Terdekat_2 = '{nama_terdekat_2}', Nama_Orang_Terdekat_3 = '{nama_terdekat_3}', 
                 Nomor_Telepon_Orang_Terdekat_1 = '{telepon_terdekat_1}', Nomor_Telepon_Orang_Terdekat_2 = '{telepon_terdekat_2}', Nomor_Telepon_Orang_Terdekat_3 = '{telepon_terdekat_3}'
    WHEN NOT MATCHED THEN
      INSERT (User_ID, Nama, Usia, Tinggi_Badan, Berat_Badan, Nama_Orang_Terdekat_1, Nama_Orang_Terdekat_2, Nama_Orang_Terdekat_3, 
              Nomor_Telepon_Orang_Terdekat_1, Nomor_Telepon_Orang_Terdekat_2, Nomor_Telepon_Orang_Terdekat_3)
      VALUES ('{user_id}', '{nama}', {usia}, {tinggi_badan}, {berat_badan}, '{nama_terdekat_1}', '{nama_terdekat_2}', '{nama_terdekat_3}', 
              '{telepon_terdekat_1}', '{telepon_terdekat_2}', '{telepon_terdekat_3}')
    """
    
    # Eksekusi query
    query_job = client.query(query)
    query_job.result()  # Tunggu hingga query selesai
    
    return jsonify({"message": "User attributes saved successfully"}), 201

def default_time_range():
    # Mengambil waktu dari 08.00 malam hingga 09.00 pagi keesokan harinya
    start_time = datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(days=1)
    return start_time, end_time

@app.route('/sleep_analysis', methods=['GET'])
def sleep_analysis():
    table_id = 'RecordPer5Menit'
    # Cek apakah ada input waktu dari pengguna
    start_time_input = request.args.get('start_time')
    end_time_input = request.args.get('end_time')

    if start_time_input and end_time_input:
        try:
            start_time = datetime.strptime(start_time_input, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_time_input, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"message": "Format waktu tidak valid. Gunakan format: YYYY-MM-DD HH:MM:SS"}), 400
    else:
        start_time, end_time = default_time_range()

    # Format waktu ke dalam format yang dapat diterima oleh BigQuery
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    # Buat query untuk mengambil data dalam rentang waktu tertentu
    query = f"""
    SELECT Sleep_Apnea, Sleep_Quality FROM `{dataset_id}.{table_id}`
    WHERE Time >= TIMESTAMP('{start_time_str}') AND Time < TIMESTAMP('{end_time_str}')
    """

    # Eksekusi query
    query_job = client.query(query)
    results = query_job.result()

    # Memeriksa apakah ada data yang ditemukan
    if results.total_rows == 0:
        return jsonify({"message": "Tidak ada data dalam rentang waktu tersebut"}), 404

    # Menghitung hasil sleep_apnea dan sleep_quality
    sleep_apnea_count = 0
    sleep_quality_good = 0
    sleep_quality_poor = 0

    for row in results:
        if row.Sleep_Apnea == 1:
            sleep_apnea_count += 1
        
        if row.Sleep_Quality == 0:
            sleep_quality_poor += 1
        elif row.Sleep_Quality == 1:
            sleep_quality_good += 1

    # Menentukan output berdasarkan hasil perhitungan
    if sleep_apnea_count > 0:
        sleep_apnea_status = "Ada sleep apnea"
    else:
        sleep_apnea_status = "Tidak ada sleep apnea"

    if sleep_quality_good > sleep_quality_poor:
        sleep_quality_status = "Kualitas tidur bagus"
    else:
        sleep_quality_status = "Kualitas tidur buruk"

    return jsonify({
        "sleep_apnea": sleep_apnea_status,
        "sleep_quality": sleep_quality_status,
        "row_found": results.total_rows
    })

@app.route('/sleep_data', methods=['GET'])
def sleep_data():
    table_id = 'RecordPer5Menit'
    # Mengambil input waktu dari parameter URL
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    if start_time_str and end_time_str:
        try:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"message": "Format waktu tidak valid. Gunakan format YYYY-MM-DD HH:MM:SS"}), 400
    else:
        # Jika tidak ada input waktu, gunakan default dari hari ini sampai keesokan harinya
        start_time = datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)

    # Format waktu ke dalam format yang dapat diterima oleh BigQuery (UTC)
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S UTC')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S UTC')

    # Buat query untuk mengambil data dalam rentang waktu tertentu
    query = f"""
    SELECT Time, HRV, SDNN, RMSSD, SDSD, pNN50, LF_HF, LF, HF, SD1, SD2, RR, murmur, Sleep_Quality, Sleep_Apnea
    FROM `{dataset_id}.{table_id}`
    WHERE Time >= TIMESTAMP('{start_time_str}') AND Time < TIMESTAMP('{end_time_str}')
    """

    # Eksekusi query
    query_job = client.query(query)
    results = query_job.result()

    if results.total_rows == 0:
        return jsonify({"message": "Tidak ada data dalam rentang waktu tersebut"}), 404

    # Mengonversi hasil query menjadi list of dictionaries untuk output JSON
    sleep_data = []
    for row in results:
        sleep_data.append({
            "Time": row.Time.strftime('%Y-%m-%d %H:%M:%S'),
            "HRV": row.HRV,
            "SDNN": row.SDNN,
            "RMSSD": row.RMSSD,
            "SDSD": row.SDSD,
            "pNN50": row.pNN50,
            "LF_HF": row.LF_HF,
            "LF": row.LF,
            "HF": row.HF,
            "SD1": row.SD1,
            "SD2": row.SD2,
            "RR": row.RR,
            "murmur": row.murmur,
            "Sleep_Quality": row.Sleep_Quality,
            "Sleep_Apnea": row.Sleep_Apnea
        })

    return jsonify({"sleep_data": sleep_data})

if __name__ == '__main__':
    app.run(debug=True)
