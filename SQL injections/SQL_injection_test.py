import os,urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import SQL_fetch
from SQL_fetch import FETCH_SQL

PORT = 8080
HOST = "localhost"
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
FETCH_SQL("create table users (id int, name varchar(32), password varchar(255));")

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
        print(query)
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
