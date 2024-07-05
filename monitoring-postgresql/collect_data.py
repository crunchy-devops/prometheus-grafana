import configparser
import psycopg2
import time
from prometheus_client import  Gauge
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)

# Initialisation de PrometheusMetrics
metrics = PrometheusMetrics(app)

# Lire les informations d'identification à partir du fichier de configuration
config = configparser.ConfigParser()
config.read('../../db_config.ini')

DB_HOST = config['postgresql']['host']
DB_NAME = config['postgresql']['database']
DB_USER = config['postgresql']['user']
DB_PASS = config['postgresql']['password']
DB_PORT = config['postgresql']['port']

# Configuration des métriques Prometheus
lock_gauge = Gauge('postgresql_locks', 'Number of locks in PostgreSQL', ['lock_type'])

def collect_locks():
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        # Exécution de la requête SQL pour obtenir les locks
        cur.execute("""
            SELECT locktype, count(*) as count
            FROM pg_locks
            GROUP BY locktype;
        """)
        # Mise à jour des métriques Prometheus
        results = cur.fetchall()
        for row in results:
            lock_gauge.labels(lock_type=row[0]).set(row[1])

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error collecting locks: {e}")


@app.route('/')
@metrics.do_not_track()  # Exclure cette route du tracking automatique
def index():
    return "Hello, World!"

@app.route('/locks')
def locks():
    collect_locks()
    return "Locks collected"


@app.route('/metrics')
def metrics_view():
    return "Custom metrics endpoint"

    # Démarrage du serveur HTTP pour exposer les métriques à Prometheus
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30800)

