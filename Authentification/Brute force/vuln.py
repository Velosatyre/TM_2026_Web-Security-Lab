from http.server import BaseHTTPRequestHandler,HTTPServer
import os,socket,urllib,webbrowser

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


#liste des utilisateurs et mots de passe autorisés
usernames = ["admin"]
credentials = {
    "admin": "admin"
}


# Chemins absolus vers les fichiers HTML utilisés par le serveur.
# On calcule ces chemins à partir du dossier contenant ce script
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
psswd = os.path.abspath(os.path.join(BASE_DIR, "home_err_psswd.html"))
usr = os.path.abspath(os.path.join(BASE_DIR, "home_err_usr.html"))
logged = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))


class web_server(BaseHTTPRequestHandler):
    """Handler HTTP minimal pour gérer GET et POST.

    - do_GET sert la page d'accueil ('home_page').
    - do_POST lit le corps d'une requête POST encodée en 'application/x-www-form-urlencoded',
        extrait 'username' et 'password', puis effectue une validation basique.
    """

    def do_GET(self):
        # Répondre 200 et renvoyer le contenu de la page d'accueil
        self.send_response(200)
        self.end_headers()
        file = open(home_page)
        # Écriture en bytes; le fichier HTML est lu en UTF-8
        self.wfile.write(bytes(file.read(), "utf-8"))

    def do_POST(self):
        # Récupération du corps de la requête
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # Parser les paramètres POST encodés (username=a&password=b)
        query = dict(urllib.parse.parse_qsl(body.decode()))

        # Extraire username / password attendus dans le formulaire
        password = query["password"]
        username = query["username"]

        # Vérification de l'existence de l'utilisateur
        if username not in usernames:
            # Utilisateur inconnu -> 401 + page d'erreur correspondante
            self.send_response(401, "Wrong username")
            self.end_headers()
            file = open(usr)
            self.wfile.write(bytes(file.read(), "utf-8"))
            return
        else:
            # Utilisateur connu -> comparer le mot de passe
            if password == credentials[username]:
                # Authentification réussie -> servir la page 'logged_in'
                self.send_response(200)
                self.end_headers()
                file = open(logged)
                self.wfile.write(bytes(file.read(), "utf-8"))
                return
            else:
                # Mauvais mot de passe -> 401 + page d'erreur
                self.send_response(401, "Wrong password")
                self.end_headers()
                file = open(psswd)
                self.wfile.write(bytes(file.read(), "utf-8"))
                return


server = HTTPServer((HOST, PORT), web_server)
# Ouvre le navigateur vers l'adresse du serveur 
#(note: le préfixe "http://" n'est pas nécessaire dans la situation d'une adresse IP)
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
# Démarre le serveur HTTP et attend les requêtes entrantes en boucle
server.serve_forever()