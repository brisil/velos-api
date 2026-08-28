import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

STATIONS_SECOURS = [
    {"id": 1, "nom": "Gare Centrale (Secours)", "velos_disponibles": 5, "emplacements_libres": 10},
    {"id": 2, "nom": "Place du Commerce (Secours)", "velos_disponibles": 0, "emplacements_libres": 15},
    {"id": 3, "nom": "Université (Secours)", "velos_disponibles": 2, "emplacements_libres": 8},
    {"id": 4, "nom": "Parc des Sports (Secours)", "velos_disponibles": 8, "emplacements_libres": 2}
]

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'db'),
            port=os.environ.get('DB_PORT', '5432'),
            database=os.environ.get('DB_NAME', 'velos'),
            user=os.environ.get('DB_USER', 'velo_user'),
            password=os.environ.get('DB_PASSWORD', 'velo_password_secret'),
            connect_timeout=3
        )
        return conn
    except Exception:
        return None

@app.route('/sante', methods=['GET'])
def sante():
    return jsonify({"statut": "OK"}), 200

@app.route('/stations', methods=['GET'])
def get_stations():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nom, velos_disponibles, emplacements_libres FROM stations;")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            stations = [{"id": r[0], "nom": r[1], "velos_disponibles": r[2], "emplacements_libres": r[3]} for r in rows]
            return jsonify({"source": "base", "version": "2.0", "stations": stations}), 200
        except Exception:
            if conn:
                conn.close()
    return jsonify({"source": "secours", "version": "2.0", "stations": STATIONS_SECOURS}), 200

@app.route('/alertes', methods=['GET'])
def get_alertes():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nom, velos_disponibles, emplacements_libres FROM stations WHERE velos_disponibles <= 2;")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            alertes = [{"id": r[0], "nom": r[1], "velos_disponibles": r[2], "emplacements_libres": r[3]} for r in rows]
            return jsonify({"source": "base", "version": "2.0", "alertes": alertes}), 200
        except Exception:
            if conn:
                conn.close()
    
    alertes_secours = [s for s in STATIONS_SECOURS if s["velos_disponibles"] <= 2]
    return jsonify({"source": "secours", "version": "2.0", "alertes": alertes_secours}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
