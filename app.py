from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# Database connection details
server = 'sleepcare.database.windows.net'
database = 'sleepcareits'
username = 'sleepcareadmin'
password = 'sayasukammsin90=1'
driver = '{ODBC Driver 17 for SQL Server}'

def get_db_connection():
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )
    return conn

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM RecordPerDay")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    events = []
    for row in rows:
        quality = "Baik" if row[2] == 1 else "Buruk"
        apnea = "Ada" if row[3] == 1 else "Tidak Ada"
        events.append({
            "title": f"Sleep Quality: {quality}, Sleep Apnea: {apnea}",
            "start": row[1].isoformat(),
            "id": row[1].isoformat()  # Use date as id
        })
    return jsonify(events)

@app.route('/api/ecg_features', methods=['GET'])
def get_ecg_features():
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Date is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    query = """
    SELECT * FROM RecordPer5Menit 
    WHERE CONVERT(date, time) = ?
    """
    cur.execute(query, (date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    features = []
    for row in rows:
        features.append({
            "id_user": row[0],
            "time": row[1].isoformat(),
            "hrv": row[2],
            "sdnn": row[3],
            "rmssd": row[4],
            "sdsd": row[5],
            "pnn50": row[6],
            "lf_hf": row[7],
            "lf": row[8],
            "hf": row[9],
            "sd1": row[10],
            "sd2": row[11],
            "rr": row[12],
            "murmur": row[13],
            "sleep_quality": row[14],
            "sleep_apnea": row[15]
        })
    return jsonify(features)

if __name__ == '__main__':
    app.run(debug=True)
