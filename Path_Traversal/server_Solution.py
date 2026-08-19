"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'acceder à des fichiers hors du serveur comme par exemple
etc/passwd

Voici comment y remédier:
Il est possible de créer une liste de paths autorisés
et de bloquer si le serveur essaye d'en accéder une autre. Malheureusement cette technique peut ralentir le processus
si le site contient beaucoup de fichiers mais cette technique bloque toute possibilité de Path Traversal.

Pour rajouter encore plus de sécurité le path qui est donné est déconstruit pour ne garder que le nom du fichier
et ensuite il est reconstruit en le joignant à un path de base (BASE_DIR) pour éviter que le serveur puisse remonter dans les dossiers. (crédit à Claude AI)
Bien sûr cela ne marche que si tout les fichiers nécessaires se trouvent dans le même dossier que le serveur.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib,os,socket, webbrowser

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

# definition du chemin des fichiers
BASE_DIR = os.path.dirname(__file__)
# liste des fichiers autorisés
AUTHORIZED_PATHS = { 
    os.path.join(BASE_DIR, "login.html"),
    os.path.join(BASE_DIR, "index.html"),
}

class Web_Server_TM(BaseHTTPRequestHandler):
    def do_GET(self):
        # analyse syntaxique de l'url
        parsed = urllib.parse.urlparse(self.path) 
        # récupère uniquement les arguments de l'url et les insère dans un dictionnaire
        query = dict(urllib.parse.parse_qsl(parsed.query)) 
        # récupère la valeur de l'argument "filename" dans le dictionnaire,
        # met "index.html" par défaut si "filename" n'est pas présent
        filename = query.get("filename", "index.html")
        # récupère uniquement le dernier nom à la fin du path
        filename = os.path.basename(filename) 
        # reconstruit le chemin complet du fichier en le joignant à BASE_DIR
        path = os.path.join(BASE_DIR, filename) 
        # convertit le chemin relatif en chemin absolu
        abs_path = os.path.abspath(path) 

        # Vérifie si le chemin absolu est dans la liste des chemins autorisés
        if abs_path not in AUTHORIZED_PATHS:
            self.send_error(403, "Access denied")
            return

        # si le chemin est autorisé, essaye d'ouvrir le fichier et de l'envoyer au client
        try:
            with open(abs_path) as f:
                content = f.read()
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, "Internal server error")


server = HTTPServer((HOST, PORT), Web_Server_TM)
webbrowser.open(HOST + ":" + str(PORT))
print("Server running")
server.serve_forever()