"""
Ce serveur est vulnérables aux injections SQL.
Il est possible de le faire à travers la page de connexion.
Le serveur prend directement les données de connexion pour les mettre dans la requête SQL, sans aucun filtrage.
"""

import os,urllib,socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from SQL_fetch import FETCH_SQL

# informations des utilisateurs
credentials = { 
    "username": [],
    "password": []
}

def IP():
# Source - https://stackoverflow.com/a/166589
# Posted by UnkwnTech, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-17, License - CC BY-SA 3.0
    """
    Retourne l'adresse IP locale de la machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))
logged_in= os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))
home_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))

# Nettoie la table sessions au cas où
FETCH_SQL("delete from users")
FETCH_SQL("insert into users values (1, 'admin', 'admin'),(2,'alice', 'password'), (3, 'bob', 'secret'), (4, 'test', 'test')")

# efface sql_requests.log
with open('SQL_requests.log', 'w'):
    pass

class WebServer(BaseHTTPRequestHandler):


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

        try:
            QueryPassword = query["password"]

        except:
            QueryPassword = ''
            
        password = FETCH_SQL("select * from users where name = '" + query["username"] + "' and password = '" + QueryPassword + "'")

        for i in password:
            username = credentials["username"]
            password = credentials["password"]

            username.append(i[1])
            password.append(i[2])

            credentials["username"] = username
            credentials["password"] = password

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


Server = HTTPServer((HOST, PORT), WebServer)

Server.serve_forever()