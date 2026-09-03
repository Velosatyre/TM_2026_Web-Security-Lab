"""
Voici un exemple d'implémentation des cookies sans aucune sécurité.
Le cookie est la variable logged_in qui représente si l'utilisateur est
connecté.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os,socket, webbrowser

"""
Retourne l'adresse IP locale de la machine.
"""
def IP():
# Source - https://stackoverflow.com/a/166589
# Posted by UnkwnTech, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-17, License - CC BY-SA 3.0

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

PORT =  8080
HOST = IP()
print("adresse du serveur: " + HOST + ":" + str(PORT))

# Chemins absolus vers les fichiers HTML utilisés
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))


class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET analyse les cookies fournit.
      regarde si le cookie logged_in est présent et si sa valeur est True ou False.
      Si le cookie n'est pas présent, il est créé avec la valeur False.
      Lors d'une tentative de connexion réussie, le cookie logged_in est mis à jour avec la valeur True.
      Dès lors que le cookie a la valeur True, l'utilisateur est considéré comme connecté et peut accéder à la page logged_in.html.
    """

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


Server = HTTPServer((HOST, PORT), WebServer)
# Ouvre le navigateur vers l'adresse du serveur
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
Server.serve_forever()