import os
import sys

from prometheus_client import Gauge
from db import conn

wal = Gauge('wal_segments', 'wal info', ['filename'])


def wal_info():
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

    except Exception as e:
        print(f"Error wal info {e}")
