
import psycopg2

from prometheus_client import Gauge
from config import DATABASE as db_config

replication = Gauge('pg_stat_replication', 'replication active', ['name'])


def pg_stat_replication():
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
                       SELECT count(*) as count
                       FROM pg_stat_replication
                    """)
        # Mise à jour des métriques Prometheus
        results = cur.fetchall()
        for row in results:
            replication.labels('replication').set(row[0])
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error pg_stat_replication: {e}")
