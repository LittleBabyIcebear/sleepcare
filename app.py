from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Database connection details
server = 'sleepcare.database.windows.net'
database = 'sleepcareits'
username = 'sleepcareadmin'
password = 'sayasukammsin90=1'
driver = 'ODBC Driver 17 for SQL Server'
connection_string = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver={driver}"

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class RecordPerDay(db.Model):
    __tablename__ = 'RecordPerDay'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    sleep_quality = db.Column(db.Integer)
    sleep_apnea = db.Column(db.Integer)

class RecordPer5Menit(db.Model):
    __tablename__ = 'RecordPer5Menit'
    id_user = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    hrv = db.Column(db.Float)
    sdnn = db.Column(db.Float)
    rmssd = db.Column(db.Float)
    sdsd = db.Column(db.Float)
    pnn50 = db.Column(db.Float)
    lf_hf = db.Column(db.Float)
    lf = db.Column(db.Float)
    hf = db.Column(db.Float)
    sd1 = db.Column(db.Float)
    sd2 = db.Column(db.Float)
    rr = db.Column(db.Float)
    murmur = db.Column(db.Integer)
    sleep_quality = db.Column(db.Integer)
    sleep_apnea = db.Column(db.Integer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ecg_features')
def about():
    return render_template('details.html')

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events_query = RecordPerDay.query.all()
        events = []
        for row in events_query:
            quality = "Baik" if row.sleep_quality == 1 else "Buruk"
            apnea = "Ada" if row.sleep_apnea == 1 else "Tidak Ada"
            events.append({
                "title": f"Sleep Quality: {quality}, Sleep Apnea: {apnea}",
                "start": row.time.isoformat(),
                "id": row.time.isoformat()  # Use date as id
            })
        return jsonify(events), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ecg_features', methods=['GET'])
def get_ecg_features():
    try:
        date = request.args.get('date')
        if not date:
            return jsonify({"error": "Date is required"}), 400

        features_query = RecordPer5Menit.query.filter(db.func.date(RecordPer5Menit.time) == date).all()
        features = []
        for row in features_query:
            features.append({
                "id_user": row.id_user,
                "time": row.time.isoformat(),
                "hrv": row.hrv,
                "sdnn": row.sdnn,
                "rmssd": row.rmssd,
                "sdsd": row.sdsd,
                "pnn50": row.pnn50,
                "lf_hf": row.lf_hf,
                "lf": row.lf,
                "hf": row.hf,
                "sd1": row.sd1,
                "sd2": row.sd2,
                "rr": row.rr,
                "murmur": row.murmur,
                "sleep_quality": row.sleep_quality,
                "sleep_apnea": row.sleep_apnea
            })
        return jsonify(features), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
