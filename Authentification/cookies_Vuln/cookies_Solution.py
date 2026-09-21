"""
Pour que les cookies ne puissent être changés pour se connecter, 
le cookie ne servira plus pour stocker la variable de connexion mais plutôt
il sera utilisé pour garder un identifiant unique généré aléatoirement.

Cet identifiant sera stocké sur le serveur et sera lui associé à la variable de connexion.
Il est donc impossible de changer le cookie pour se connecter, 
par contre, théoriquement, il est possible de voler l'identifiant d'un utilisateur connecté. 
Il faudrait faire que les identifiants changent de temps en temps 
pour rendre encore plus difficile ces modifications. 

Pour cela, il y a la possibilité de définir un temps de vie pour le cookie.
Il sera automatiquement supprimé après le temps défini.

De plus le login form à la place d'envoyer une requête GET, il envoie une requête POST. 
Cela enlève les variables de l'url ce qui supprime la possibilité de modifier ces valeurs plus tard.

Cela permet aussi à un utilisateur de pouvoir juste relancer la page après que son cookies expire
et il peut refaire la connexion. Déconnexion après un certains temps.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os, urllib, secrets

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "homepost.html"))
home_page_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))
home_page_exp = os.path.abspath(os.path.join(BASE_DIR, "home_exp.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))

# SSID des utilisateurs connectés
SESSION_ID = {

}

Users = {
    "admin": "admin",
    "alice": "123",
    "test":  "test"
}

"""
Génère un identifiant randomisé
"""
def SSID_Generator():
    SSID = secrets.token_urlsafe(16)
    return SSID

class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET analyse les cookies fournit.
      regarde si le cookie SSID est présent et si sa valeur est dans la liste des SESSION
      Si le cookie n'est pas présent, il est créé avec la fonction SSID_Generator.
      
    - do_POST analyse les données du formulaire de connexion.
      Si le nom d'utilisateur et le mot de passe sont corrects, 
      le cookie SSID de l'utilisateur est ajouté dans la liste des utilisateurs connectés.
    """

    def do_GET(self):
        cookies = SimpleCookie(self.headers.get("Cookie"))
        file = home_page
        
        if "SSID" in cookies:
            if cookies["SSID"].value in SESSION_ID:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                file = logged_in_page

            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                file = home_page_err

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        
        files = open(file)
        self.wfile.write(bytes(files.read(), "utf-8"))


    def do_POST(self): # Aidé par Chatgpt 5.5 pour l'idée de la fonction, le 12.5.2026
        file = home_page

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            query = dict(urllib.parse.parse_qsl(body.decode()))

            try:
                username = query["user"]
                password = query["pass"]
 
                if username in Users and password == Users[username]:
                    SSID = SSID_Generator()
                    SESSION_ID[SSID] = username

                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    # Gemini a ajouté, le 9.9.2026: HttpOnly, Secure, SameSite=Strict
                    self.send_header("Set-Cookie", f"SSID={SSID} ; max-age=60 ; HttpOnly ; SameSite=Strict ; Secure")
                    self.end_headers()

                    file = logged_in_page

                else:
                        self.send_response(401)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()

                        file = home_page_err

            except:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                file = home_page

        except:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            file = home_page

        files = open(file)
        self.wfile.write(bytes(files.read(), "utf-8"))




Server = HTTPServer((HOST, PORT), WebServer)

Server.serve_forever()