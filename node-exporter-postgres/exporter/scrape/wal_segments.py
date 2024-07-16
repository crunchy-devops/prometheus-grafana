
import psycopg2

from prometheus_client import Gauge
from config import DATABASE as db_config

wal = Gauge('wal_segments', 'wal info', ['filename'])


def wal_info():
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            dbname=db_config['name'],
            user=db_config['user'],
            password=db_config['pass']
        )
    except Exception as e:
        print(f"Error connection {e}")

    try:
        cur = conn.cursor()
        # Exécution de la requête SQL pour obtenir les locks
        cur.execute("""
                      SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0');
                    """)
        # Mise à jour des métriques Prometheus
        results = cur.fetchall()
        for row in results:
            #filename = row[0]
            size = int(row[0]) / 1024 / 1024
            wal.labels(filename='wal').set(size)
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error wal info {e}")
