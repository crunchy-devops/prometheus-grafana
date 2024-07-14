from config import DATABASE as db_config
import psycopg2


try:
    # Connexion à la base de données PostgreSQL
    conn = psycopg2.connect (
        host=db_config['host'],
        port=db_config['port'],
        dbname=db_config['name'],
        user=db_config['user'],
        password=db_config['pass']
    )
except Exception as e:
    print(f"Error connection {e}")