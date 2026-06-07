import os,urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import SQL_fetch
from SQL_fetch import FETCH_SQL
import subprocess as sub

PORT = 8080
HOST = "localhost"
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))

class Web_Server_TM(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        file = open(home_page)
        self.wfile.write(bytes(file.read(), "utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        query = dict(urllib.parse.parse_qsl(body.decode()))
        FETCH_SQL("select password from users where name = '" + query["username"] + "';")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        file = open(home_page)
        self.wfile.write(bytes(file.read(), "utf-8"))


server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")
