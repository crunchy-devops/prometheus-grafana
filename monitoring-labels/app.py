from prometheus_client import start_http_server, Gauge
import time

# Configuration des labels et du numéro de version
VERSION = "3.0.0"
LABELS = {
    'app_name': 'my_application',
    'environment': 'production',
    'version': VERSION,
}

# Configuration des métriques Prometheus
version_info = Gauge('application_version_info', 'Version information of the application', list(LABELS.keys()))


def set_version_metric():
    # Mise à jour des métriques Prometheus avec le numéro de version et les labels
    version_info.labels(**LABELS).set(1)


if __name__ == '__main__':
    # Démarrage du serveur HTTP pour exposer les métriques à Prometheus
    start_http_server(30805)
    print("Starting version exporter on port 308005")

    # Initialiser la métrique avec le numéro de version
    #set_version_metric()

    # Garder le programme en cours d'exécution
    while True:
        set_version_metric()
        time.sleep(5)
