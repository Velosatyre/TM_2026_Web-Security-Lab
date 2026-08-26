"""
Afin de contrôler si un cookie a été changé, l'idée est de faire un hash du cookie qui est envoyé.
Quand le client fera une requête, le serveur va alors hasher le cookie qu'il reçoit
et le comparer au sien.
Pour plus de sécurité, le serveur ne conserve uniquement les hash des passwords.
De plus le login form à la place d'envoyer une requête GET il envoie une requête POST. 
Cela enlève les variables de l'url ce qui supprime la possibilité de modifier ces valeurs plus tard.
Cela permet aussi à un utilisateur de pouvoir juste relancer la page après que son cookies expire
et il peut refaire la connexion. Déconnexion après un certains temps.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os, urllib, secrets, hashlib, socket, webbrowser


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
home_page = os.path.abspath(os.path.join(BASE_DIR, "homepost.html"))
home_page_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))
home_page_exp = os.path.abspath(os.path.join(BASE_DIR, "home_exp.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))

# SSID des utilisateurs connectés
SESSION_ID = {

}
"""
prend en entrée une chaîne de caractères (le mot de passe) et retourne son hash SHA-256.
"""
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
# les mots de passes gardés sous forme de hash
Users = {
    "admin": hash_password("admin"),
    "alice": hash_password("123"),
    "test":  hash_password("test")
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


    def do_POST(self): # Aidé par IA
        file = home_page
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            query = dict(urllib.parse.parse_qsl(body.decode()))

            try:
                username = query["user"]
                submitted_hash = hash_password(query["pass"])
 
                if username in Users and submitted_hash == Users[username]:
                    SSID = SSID_Generator()
                    SESSION_ID[SSID] = username
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Set-Cookie", f"SSID={SSID} ; max-age=60")
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
# Ouvre le navigateur vers l'adresse du serveur 
# (note: le préfixe "http://" n'est pas nécessaire dans la situation d'une adresse IP)
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
# Démarre le serveur HTTP et attend les requêtes entrantes en boucle
Server.serve_forever()