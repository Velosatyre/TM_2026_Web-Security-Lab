"""
Une des solutions possibles est de filtrer les caractères spéciaux dans les entrées utilisateur. Cependant, cette solution est très fragile et peut être contournée de différentes manières. 
Par exemple, un attaquant pourrait utiliser des encodages alternatifs pour contourner les filtres, ou trouver d'autres caractères spéciaux qui ne sont pas filtrés.
Une manière meilleure mais plus lente consiste à créer une liste de caractères autorisés et les filtrer.

Autre solution : hasher les infos des utilisateurs dans la database et aussi hasher ce que les clients envoient.

La méthode la plus simple et la plus rapide est d'utiliser les données comme paramètres. 
"""

import os,urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from SQL_fetch import FETCH_SQL

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))
logged_in= os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))
home_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))

# Nettoie la table sessions au cas où
FETCH_SQL("delete from users")
FETCH_SQL("insert into users values (1, 'admin', 'admin'),(2,'alice', 'password'), (3, 'bob', 'secret'), (4, 'test', 'test')")

#liste des caractères autorisés
allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

with open('/app/log/SQL_requests.log', 'w'):
    pass

class WebServerParameters(BaseHTTPRequestHandler):
    """
    - do_GET envoie la page principale
    
    - do_POST récupère les données du formulaire de connexion,
      puis exécute une requête SQL pour vérifier si l'utilisateur existe et si le mot de passe correspond. 
      Au lieu de filtrer les caractères spéciaux, la requête SQL utilise des paramètres pour éviter les injections SQL.
    """

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

        try :
            SQLusername = FETCH_SQL("select password from users where name = %s", (username,))

        except:
            SQLusername = []

        if len(SQLusername) > 0 and SQLusername[0][0] == query["password"]:
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


Server = HTTPServer((HOST, PORT), WebServerParameters)

Server.serve_forever()
