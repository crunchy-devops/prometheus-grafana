from prometheus_client import start_http_server, Gauge
import time
import configparser
import psycopg2

# Configuration des labels et du numéro de version
VERSION = "3.0.0"
STATS = {
    'app_name': 'my_application',
    'environment': 'production',
    'version': VERSION,
}
LABELS = {
    'replication': 'replication',
}

# Lire les informations d'identification à partir du fichier de configuration
config = configparser.ConfigParser()
config.read('../../db_config.ini')

DB_HOST = config['postgresql']['host']
DB_NAME = config['postgresql']['database']
DB_USER = config['postgresql']['user']
DB_PASS = config['postgresql']['password']
DB_PORT = config['postgresql']['port']


# Configuration des métriques Prometheus
version_info = Gauge('application_version_info', 'Version information of the application', list(STATS.keys()))
replication  = Gauge('pg_stat_replication', 'replication active', ['name'])
locks        = Gauge('pg_locks', 'replication active', ['datname','mode'])
# Configuration des métriques Prometheus
db_size_gauge = Gauge( 'postgres_database_size_bytes','Size of PostgreSQL databases in bytes', ['database_name'])
def set_version_metric():
    # Mise à jour des métriques Prometheus avec le numéro de version et les labels
    version_info.labels(**STATS).set(1)

def pg_stat_replication():
    labels = []
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
               SELECT count(*) as count
               FROM pg_stat_replication
           """)
        # Mise à jour des métriques Prometheus
        results = cur.fetchall()
        for row in results:
            replication.labels('kitchen').set(row[0])


        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error pg_stat_replication: {e}")

#---------------------------------------------------------------------------
#   Locks
#---------------------------------------------------------------------------
def pg_locks():
    labels = []
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
        cur.execute("""SELECT 
		  pg_database.datname as datname,
		  tmp.mode as mode,
		  COALESCE(count, 0) as count 
		FROM 
		  (
		    VALUES 
		      ('accesssharelock'), 
		      ('rowsharelock'), 
		      ('rowexclusivelock'), 
		      ('shareupdateexclusivelock'), 
		      ('sharelock'), 
		      ('sharerowexclusivelock'), 
		      ('exclusivelock'), 
		      ('accessexclusivelock'), 
		      ('sireadlock')
		  ) AS tmp(mode)
		  CROSS JOIN pg_database 
		  LEFT JOIN (
		    SELECT 
		      database, 
		      lower(mode) AS mode, 
		      count(*) AS count 
		    FROM 
		      pg_locks 
		    WHERE 
		      database IS NOT NULL 
		    GROUP BY 
		      database, 
		      lower(mode)
		  ) AS tmp2 ON tmp.mode = tmp2.mode 
		  and pg_database.oid = tmp2.database 
		ORDER BY 
		  1
           """)
        # Mise à jour des métriques Prometheus
        results = cur.fetchall()
        for row in results:
            locks.labels(datname=row[0],mode=row[1]).set(row[2])

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error pg_locks: {e}")

#-----------------------------------------------------------------
# fetch db size
#----------------------------------------------------------------
def fetch_db_sizes():
    """Fetch sizes of PostgreSQL databases and update Prometheus metrics."""
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()

        # Exécuter la requête pour obtenir les tailles des bases de données
        cursor.execute("""
            SELECT datname, pg_database_size(datname)
            FROM pg_database
            WHERE datistemplate = false;
        """)
        rows = cursor.fetchall()

        # Mettre à jour les métriques Prometheus
        for row in rows:
            database_name, size_bytes = row
            size_bytes = size_bytes / 1024 / 1024
            db_size_gauge.labels(database_name=database_name).set(size_bytes)

        # Fermer la connexion
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == '__main__':
    # Démarrage du serveur HTTP pour exposer les métriques à Prometheus
    start_http_server(30808)
    print("Starting version exporter on port 30808")

    # Initialiser la métrique avec le numéro de version
    #set_version_metric()

    # Garder le programme en cours d'exécution
    while True:
        set_version_metric()
        pg_stat_replication()
        pg_locks()
        fetch_db_sizes()
        time.sleep(5)
