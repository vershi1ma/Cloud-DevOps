from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            "message": "Hello from the backend service - v2",
            "server_time_utc": datetime.now(timezone.utc).isoformat()
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 5000), Handler).serve_forever()
