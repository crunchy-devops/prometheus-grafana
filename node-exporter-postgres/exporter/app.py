import time

from prometheus_client import start_http_server
from scrape.replication import pg_stat_replication
from scrape.locks import pg_locks
from  scrape.wal_segments import wal_info
def main():
    start_http_server(30808)
    print("Starting version exporter on port 30808")
    while True:
        pg_stat_replication()
        pg_locks()
        wal_info()
        time.sleep(5)

if __name__ == '__main__':
    main()