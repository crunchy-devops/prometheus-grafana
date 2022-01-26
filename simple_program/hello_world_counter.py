import http.server
from prometheus_client import start_http_server, Counter

REQUEST = Counter('hello_worlds_total', 'Hello Worlds requested.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUEST.inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == "__main__":
    start_http_server(18000)
    server = http.server.HTTPServer(('', 18081), MyHandler)
    server.serve_forever()

