"""
Il suffit que la requête ver la base de données ne soit pas directe. Il faut aussi exactement comparer ce que l'utilisateur envoit avec ce que la base de données contient.
Nouvelle possibilité d'injection : pseudo : ' or 1=1;-- password : il faut avoir le code de l'utilisateur ayant l'id = 1
"""

import os,urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import SQL_fetch
from SQL_fetch import FETCH_SQL
import subprocess as sub

PORT = 8080
HOST = "localhost"
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))
logged_in= os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))
home_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))
FETCH_SQL("delete from users;")
FETCH_SQL("insert into users values (1, 'admin', 'admin'),(2,'alice', 'password'), (3, 'bob', 'secret'), (4, 'test', 'test');")

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
        username = str(query["username"])
        print(query)
        print("select * from users where name = '" + username+"';")
        data = FETCH_SQL("select * from users where name = '" + username +"';")
        print(data)
        
        if len(data) > 0 and data[0][2] == query["password"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(logged_in)
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(home_err)
        self.wfile.write(bytes(file.read(), "utf-8"))


server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")
