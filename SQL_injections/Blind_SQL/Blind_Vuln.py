"""
Pour cette vulnérabilité il faudra utiliser BurpSuite community afin d'automatiser les attaques
Le concept d'une injection SQL à l'aveugle est qu'il n'y pas de retour instantané lorsqu'on ajoute un SQL payload.

Dans cette situation il y a un cookie qui détermine si l'utilisateur est déjà allé sur le site.
lors d'une connexion le serveur va regarder dans une table nommée sessions si le cookie est présent dans la table. Si oui alors l'utilisateur recevra un message "Welcome back".
La page web ne retourne pas la réponse de la requête SQL mais en fonction de la réponse la page sera différente.
Les injections à l'aveugle sont du tâtonnement et pour le faire je vous conseille d'utiliser BurpSuite, car l'outil va automatiser les énumérations.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from SQL_fetch import FETCH_SQL
import os,secrets,socket



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
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))

# Nettoie la table sessions au cas où
FETCH_SQL("delete from sessions")
FETCH_SQL("create table if not exists sessions (SSID varchar(255))")

with open('/app/log/SQL_requests.log', 'w'):
    pass

"""
Génère un SSID aléatoire pour l'utilisateur.
"""
def SSID_Generator():
    SSID = secrets.token_urlsafe(16)
    return SSID

class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET récupère le cookie de la requête.
      Si le cookie n'est pas présent ou si le cookie n'est pas dans la liste,
      alors il génère un nouveau ID et l'insère dans la table sessions.
      Si le cookie est présent et qu'il est dans la table sessions,
      alors l'utilisateur reçoit un message "Welcome back".
    """

    def do_GET(self):
        cookies = SimpleCookie(self.headers.get("Cookie"))

        if not "SSID" in cookies:
            SSID = SSID_Generator()

            self.send_response(200)
            self.send_header("Set-Cookie", f"SSID={SSID};")
            self.send_header("Content-type", "text/html")
            self.end_headers()

            file = open(home_page)
            html = file.read().format(message="WELCOME")

            FETCH_SQL("insert into sessions (SSID) values ('" + SSID + "')")

        else:
            SSID = cookies["SSID"].value
            sessions = FETCH_SQL("select * from sessions where ssid='"+SSID+"'")

            if sessions == None:
                SSID = SSID_Generator()

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Set-Cookie", f"SSID={SSID};")
                self.end_headers()

                file = open(home_page)
                html = file.read().format(message="WELCOME")

                FETCH_SQL("insert into sessions (SSID) values ('" + SSID + "')")

            elif len(sessions) > 0:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                file = open(home_page)

                html = file.read().format(message="WELCOME BACK")
            else:
                SSID = SSID_Generator()

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Set-Cookie", f"SSID={SSID};")
                self.end_headers()

                file = open(home_page)
                html = file.read().format(message="WELCOME")

                FETCH_SQL("insert into sessions (SSID) values ('" + SSID + "')")

        self.wfile.write(bytes(html, "utf-8"))  
        


Server = HTTPServer((HOST, PORT), WebServer)

Server.serve_forever()