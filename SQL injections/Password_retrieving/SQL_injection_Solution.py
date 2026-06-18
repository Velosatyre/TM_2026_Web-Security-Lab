"""
Une des solutions possibles est de filtrer les caractères spéciaux dans les entrées utilisateur. Cependant, cette solution est très fragile et peut être contournée de différentes manières. 
Par exemple, un attaquant pourrait utiliser des encodages alternatifs pour contourner les filtres, ou trouver d'autres caractères spéciaux qui ne sont pas filtrés.
Une manière meilleure mais plus lente consiste à créer une liste de charactères autorisés et les filtrer.

Autre solution : hasher les infos des utilisateurs dans la database et aussi hasher ce que les clients envoyent.
La méthode la plus simple et la plus rapide est d'utiliser les données comme paramètres. 
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
allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
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
        username = str(query["username"])
        print(username)
        username = ''.join(c for c in username if c in allowed_chars)
        print(username)
        try :
            usr = FETCH_SQL("select * from users where name = '" + username + "';")
        except:
            usr = []
        print(usr)
        if len(usr) > 0 and usr[0][2] == query["password"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(logged_in)
            html = file.read().format(username=username,password=query["password"])
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(home_err)
            html = file.read()
        self.wfile.write(bytes(html, "utf-8"))

class Web_Server_TM_paramètres(BaseHTTPRequestHandler):
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
        print(username)
        try :
            usr = FETCH_SQL("select password from users where name = %s;", (username))
        except:
            usr = []
        print(usr)
        if len(usr) > 0 and usr[0][0] == query["password"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(logged_in)
            html = file.read().format(username=username,password=query["password"])
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(home_err)
            html = file.read()
        self.wfile.write(bytes(html, "utf-8"))


server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")
