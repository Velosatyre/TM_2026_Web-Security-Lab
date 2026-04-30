"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'acceder à des fichiers hors du serveur comme par exemple
etc/passwd

Voici comment y remedier:
Il est possible de créer une liste de paths autorisés
et de bloquer si le serveur essaye d'en accéder une autre. Malheureseument cette technique peut ralentir le processus
si le site contient beacoup de fichiers mais cette technique bloque toute possibilié de Path Traversal.

Pour rajouter encore plus de sécurité le path qui est donné est déconstruit pour ne garder que le nom du fichier
et ensuite il est reconstruit en le joignant à un path de base (BASE_DIR) pour éviter que le serveur puisse remonter dans les dossiers. (crédit à Claude AI)
Biensûr cela ne marche que si tout les fichiers nécessaires se trouvent dans le même dossier que le serveur.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import os

PORT = 8080
HOST = "localhost"

BASE_DIR = os.path.abspath(".") # récupère la chemin absolu dans lequel se trouve le serveur.
#print("Base directory:", BASE_DIR)
AUTHORIZED_PATHS = { # liste des fichiers autorisés
    os.path.join(BASE_DIR, "login.html"),
    os.path.join(BASE_DIR, "index.html"),
}

class Web_Server_TM_Netcat_V1(BaseHTTPRequestHandler):
    def  do_GET(self):
        parsed = urllib.parse.urlparse(self.path) # analyse syntaxique de l'url
        path = parsed.path # récupère uniquement le path de l'url
        filename = os.path.basename(path) # récupère uniquement le nom du fichier dans le path
        print(filename)
        path = os.path.join(BASE_DIR, filename) # reconstruit le chemin complet du fichier en le joignant à BASE_DIR
        print(path)
        abs_path = os.path.abspath(path) # convertit le chemin relatif en chemin absolu

        # Vérifie si le chemin absolu est dans la liste des chemins autorisés
        if abs_path not in AUTHORIZED_PATHS:
            self.send_error(403, "Access denied")
            return

        # si le chemin est autorisé, essaye d'ouvrir le fichier et de l'envoyer au client
        try:
            with open(abs_path, "r") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

class Web_Server_TM_Web_browser_V1(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path) # analyse syntaxique de l'url
        query = dict(urllib.parse.parse_qsl(parsed.query)) # récupère uniquement les arguments de l'url et les insère dans un dictionnaire
        filename = query.get("filename", "index.html")# récupère la valeur de l'argument "filename" dans le dictionnaire, met "index.html" par défaut si "filename" n'est pas présent
        filename = os.path.basename(filename) # récupère uniquement le dernier nom à la fin du path
        path = os.path.join(BASE_DIR, filename) # reconstruit le chemin complet du fichier en le joignant à BASE_DIR
        abs_path = os.path.abspath(path) # convertit le chemin relatif en chemin absolu

        # Vérifie si le chemin absolu est dans la liste des chemins autorisés
        if abs_path not in AUTHORIZED_PATHS:
            self.send_error(403, "Access denied")
            return

        # si le chemin est autorisé, essaye d'ouvrir le fichier et de l'envoyer au client
        try:
            with open(abs_path, "r") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")


server = HTTPServer((HOST, PORT), Web_Server_TM_Web_browser_V1)
print("Server running")
server.serve_forever()