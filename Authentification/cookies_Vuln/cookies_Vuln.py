"""
Voici un exemple d'implementation des cookies sans aucune sécurité.
Le cookie est la variable logged_in qui représente si l'utilisateur est
connecté. Pour ce connecter sans code il suffit d'inspecter la page, et aller dans storage.
La bas il y aura le cookie. Il faut juste changer la valeur de False a True.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os,socket, webbrowser


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


class Web_Server_TM(BaseHTTPRequestHandler):

    def do_GET(self):
        cookies = SimpleCookie(self.headers.get("Cookie"))
        file = home_page

        if "logged_in" in cookies:
            logged_in_cookie = cookies["logged_in"].value
            
            if logged_in_cookie == "True":
                file = logged_in_page

            elif logged_in_cookie == "False":
                file = home_page

            self.send_response(200)
            self.send_header("content-type", "text/html")

        if not "logged_in" in cookies:
            self.send_response(200)
            self.send_header("Set-Cookie", "logged_in=False ; max-age=60")

        try:
            file = open(file)
            file = file.read()
        except FileNotFoundError:
            self.send_error(404, "Page not found")
            return
        
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))


server = HTTPServer((HOST,PORT), Web_Server_TM)
webbrowser.open(HOST + ":" + str(PORT))
print("server running")
server.serve_forever()