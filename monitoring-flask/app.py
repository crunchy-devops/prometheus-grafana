from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram

app = Flask(__name__)

# Initialisation de PrometheusMetrics
metrics = PrometheusMetrics(app)

# Compteur personnalisé
request_counter = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'])

# Histogramme personnalisé
request_latency = Histogram('http_request_latency_seconds', 'HTTP request latency', ['endpoint'])

@app.route('/')
@metrics.do_not_track()  # Exclure cette route du tracking automatique
def index():
    return "Hello, World!"

@app.route('/status')
def status():
    request_counter.labels(method='GET', endpoint='/status').inc()
    with request_latency.labels(endpoint='/status').time():
        return "Status: OK"

@app.route('/metrics')
def metrics_view():
    return "Custom metrics endpoint"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31500)
