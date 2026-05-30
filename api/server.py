from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from auth import check_auth

# in-memory DB
transactions = {}


def unauthorized(self):
    self.send_response(401)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(b'{"error":"Unauthorized"}')


class APIHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        if not check_auth(self.headers):
            unauthorized(self)
            return

        if self.path == "/transactions":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(list(transactions.values())).encode())
            return

        if self.path.startswith("/transactions/"):
            tx_id = self.path.split("/")[-1]

            if tx_id in transactions:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(transactions[tx_id]).encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error":"Not found"}')
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'{"error":"Invalid endpoint"}')

    # POST
    def do_POST(self):

        if not check_auth(self.headers):
            unauthorized(self)
            return

        if self.path == "/transactions":
            length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(length)
            data = json.loads(body)

            tx_id = str(data["id"])
            transactions[tx_id] = data

            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Created", "data": data}).encode())
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'{"error":"Invalid endpoint"}')

    # PUT
    def do_PUT(self):

        if not check_auth(self.headers):
            unauthorized(self)
            return

        if self.path.startswith("/transactions/"):
            tx_id = self.path.split("/")[-1]

            if tx_id not in transactions:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error":"Not found"}')
                return

            length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(length)
            data = json.loads(body)

            transactions[tx_id] = data

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Updated", "data": data}).encode())
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'{"error":"Invalid endpoint"}')

    # DELETE
    def do_DELETE(self):

        if not check_auth(self.headers):
            unauthorized(self)
            return

        if self.path.startswith("/transactions/"):
            tx_id = self.path.split("/")[-1]

            if tx_id in transactions:
                del transactions[tx_id]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"message":"Deleted"}')
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error":"Not found"}')
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'{"error":"Invalid endpoint"}')


def run():
    server = HTTPServer(("0.0.0.0", 8000), APIHandler)
    print("Server running on port 8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
