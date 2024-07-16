import psycopg2

from prometheus_client import Gauge
from config import DATABASE as db_config

locks        = Gauge('pg_locks', 'replication active', ['datname','mode'])

def pg_locks():
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