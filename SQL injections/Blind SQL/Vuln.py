"""
Pour cette vulnérabilité il faudra utiliser burpsuite community afin d'automatiser les attaques
Le concept d'une injection SQL à l'aveugle est qu'il n'y pas de retour instantané lorsqu'on ajoute un SQL payload.
Dans cette situation il y a un cookie qui détermine si l'utilisateur est déjà allé sur le site.
lors d'une connexion le serveur va regarder dans une table nommée sessions si le cookie est présent dans la table. Si oui alors l'utilisateur recevra un message "Welcome back".
La page web ne retourne pas la réponse de la requête SQL mais en fonction de la réponse la page sera différente.
Les injections à l'aveugle sont du tâtonnement et pour le faire je vous conseille d'utiliser BurpSuite, car l'outil va automatiser les énumérations.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os,secrets,socket
from SQL_fetch import FETCH_SQL


PORT = 8080
# L'adresse locale est donnée, car pour intercepter les requêtes avec BurpSuite il faut le faire au travers de l'adresse locale.
def IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    IP = s.getsockname()[0]
    return IP

HOST = IP()

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))

FETCH_SQL("delete from sessions;")
FETCH_SQL("create table if not exists sessions (SSID varchar(255));")

with open('SQL_requests.log', 'w'):
    pass

def SSID_Generator():
    SSID = secrets.token_urlsafe(16)
    return SSID

class Web_Server_TM(BaseHTTPRequestHandler):

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
            FETCH_SQL("insert into sessions (SSID) values ('" + SSID + "')")
            print("done")
        else:
            SSID = cookies["SSID"].value
            print(SSID)
            sessions = FETCH_SQL("select * from sessions where ssid='"+SSID+"'")
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
        


server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")