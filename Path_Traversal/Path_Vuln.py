"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'accéder à des fichiers hors du serveur comme par exemple
le fichier passwd qui contient des informations sur les utilisateurs du système.
Il se trouve dans le répertoire /etc/passwd sur les systèmes Linux.



"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib,os

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")

# definition du chemin des fichiers
BASE_DIR = os.path.dirname(__file__)
index_page = os.path.abspath(os.path.join(BASE_DIR, "index.html"))
login_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))


class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET analyse l'url de la requête.
      récupère le nom du fichier demandé dans les arguments de l'url
      et envoie le fichier demandé au client.
    """
    def do_GET(self):
        self.send_response(200) 
        self.send_header("content-type", "text/html") 
        self.end_headers()

        parsed = urllib.parse.urlparse(self.path)
        query = dict(urllib.parse.parse_qsl(parsed.query)) 
        filename = query.get("filename", "index.html")

        try:
            filename = os.path.join(BASE_DIR,query.get("filename"))
        except:
            filename = os.path.join(BASE_DIR,"index.html")
        
        try:
            file = open(filename)
        except:
            file = open(index_page) 
        finally:
            self.wfile.write(bytes(file.read(), "utf-8"))



Server = HTTPServer((HOST, PORT), WebServer)

Server.serve_forever()