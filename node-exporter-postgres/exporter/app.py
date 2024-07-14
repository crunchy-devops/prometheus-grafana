import time

from prometheus_client import start_http_server
from scrape.replication import pg_stat_replication

def main():
    start_http_server(30808)
    print("Starting version exporter on port 30808")
    while True:
        pg_stat_replication()
        time.sleep(5)

if __name__ == '__main__':
    main()