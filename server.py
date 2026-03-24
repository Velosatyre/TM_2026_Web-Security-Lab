from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8080
HOST = "localhost"

class Web_Server_TM(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        
        self.wfile.write(bytes("<html><body><h1>HELLO WOLRD</h1></body></html>", "utf-8"))



server = HTTPServer((HOST,PORT), Web_Server_TM)
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")