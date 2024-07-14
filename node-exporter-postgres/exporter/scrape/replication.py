import os
import sys

from prometheus_client import Gauge

from db import conn

replication = Gauge('pg_stat_replication', 'replication active', ['name'])


def pg_stat_replication():
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

    except Exception as e:
        print(f"Error pg_stat_replication: {e}")
