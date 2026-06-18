"""
SQL injection, 
Comment : pseudo : admin';--
    code : ce que vous voulez
il est important de mettre après le pseudo ';-- 

Comment : pseudo : ' or 1=1;--  
    password : ce que vous voulez
"""

import os,urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from SQL_fetch import FETCH_SQL

credentials = { 
    "username": [],
    "password": []
}

PORT = 8080
HOST = "localhost"

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))
logged_in= os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))
home_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))

FETCH_SQL("delete from users;")
FETCH_SQL("insert into users values (1, 'admin', 'admin'),(2,'alice', 'password'), (3, 'bob', 'secret'), (4, 'test', 'test');")
# efface sql_requests.log
with open('SQL_requests.log', 'w'):
    pass

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
        #print(query["password"])
        #print("select * from users where name = '" + query["username"] + "' and password = '" + query["password"] + "';")
        password = FETCH_SQL("select * from users where name = '" + query["username"] + "' and password = '" + query["password"] + "';")
        #print(password)
        for i in password:
            usr = credentials["username"]
            pswd = credentials["password"]
            usr.append(i[1])
            pswd.append(i[2])
            credentials["username"] = usr
            credentials["password"] = pswd
        if len(password) > 0:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(logged_in)
            html = file.read().format(**credentials)
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(home_err)
            html = file.read()
        self.wfile.write(bytes(html, "utf-8"))
        credentials["username"] = []
        credentials["password"] = []


server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")
