import os
import sys

from prometheus_client import Gauge

# Obtenir le chemin absolu du répertoire principal
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Ajouter le répertoire principal au chemin de recherche de modules
sys.path.insert(0, main_directory)

# Importer le module db
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
