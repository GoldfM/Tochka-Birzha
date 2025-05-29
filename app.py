from http.server import BaseHTTPRequestHandler, HTTPServer

class TestHandler(BaseHTTPRequestHandler):
    def Req_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Base")
        elif self.path == '/about':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"About")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Err")

    def Req_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_d = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Data: " + post_d)



server = HTTPServer(('localhost', 8080), SimpleHandler)
print("Starting server on http://localhost:8080")
server.serve_forever()