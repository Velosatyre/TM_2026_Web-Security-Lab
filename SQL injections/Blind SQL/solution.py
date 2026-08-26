

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os,secrets,socket, webbrowser
from SQL_fetch import FETCH_SQL


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

PORT =  8080
HOST = IP()
print("adresse du serveur: " + HOST + ":" + str(PORT))

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))

# Nettoie la table sessions au cas où
FETCH_SQL("delete from sessions")
FETCH_SQL("create table if not exists sessions (SSID varchar(255))")

with open('SQL_requests.log', 'w'):
    pass
"""
Génère un SSID aléatoire pour l'utilisateur.
"""
def SSID_Generator():
    SSID = secrets.token_urlsafe(16)
    return SSID

class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET analyse les cookies fournit.
      regarde si le cookie SSID est présent et si sa valeur est dans la table sessions avec une requête SQL.
      Si le cookie n'est pas présent, il est créé avec un SSID aléatoire.
    
    """

    def do_GET(self):
        cookies = SimpleCookie(self.headers.get("Cookie"))
        if not "SSID" in cookies:
            print("no cookie")
            SSID = SSID_Generator()
            self.send_response(200)
            self.send_header("Set-Cookie", f"SSID={SSID};")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(home_page)
            html = file.read().format(message="WELCOME")
            FETCH_SQL("insert into sessions (SSID) values (%s)", (SSID,))
            print("done")
        else:
            SSID = cookies["SSID"].value
            print(SSID)
            sessions = FETCH_SQL("select * from sessions where SSID = (%s)", (SSID,))
            print(sessions)
            if sessions == None:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                SSID = SSID_Generator()
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
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                SSID = SSID_Generator()
                self.send_header("Set-Cookie", f"SSID={SSID};")
                self.end_headers()
                file = open(home_page)
                html = file.read().format(message="WELCOME")
                FETCH_SQL("insert into sessions (SSID) values ('" + SSID + "')")

        self.wfile.write(bytes(html, "utf-8"))  
        


Server = HTTPServer((HOST, PORT), WebServer)
# Ouvre le navigateur vers l'adresse du serveur 
# (note: le préfixe "http://" n'est pas nécessaire dans la situation d'une adresse IP)
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
# Démarre le serveur HTTP et attend les requêtes entrantes en boucle
Server.serve_forever()