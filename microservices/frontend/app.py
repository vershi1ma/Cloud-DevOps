from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend-service:5000")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with urllib.request.urlopen(BACKEND_URL, timeout=3) as resp:
                data = json.loads(resp.read())
            message = data.get("message", "")
            server_time = data.get("server_time_utc", "")
            status = "reached backend successfully"
        except Exception as e:
            message = "could not reach backend"
            server_time = ""
            status = f"error: {e}"

        html = f"""<!DOCTYPE html>
<html>
<head><title>Frontend Service</title></head>
<body>
  <h1>Frontend Service</h1>
  <p>Status: {status}</p>
  <p>Backend says: {message}</p>
  <p>Backend server time (UTC): {server_time}</p>
</body>
</html>"""
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 5000), Handler).serve_forever()
