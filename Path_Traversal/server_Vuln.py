"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'accéder à des fichiers hors du serveur comme par exemple
le fichier passwd qui contient des informations sur les utilisateurs du système.
Il se trouve dans le répertoire /etc/passwd sur les systèmes Linux.



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

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")
print("adresse du serveur: " + HOST + ":" + str(PORT))

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
        # envoie une réponse 200 (ok)
        self.send_response(200) 
        # envoi un header avec comme variable en plus le content-type qui est du html
        self.send_header("content-type", "text/html") 
        self.end_headers()

        # analyse syntaxique de l'url
        parsed = urllib.parse.urlparse(self.path)
        # récupère uniquement les arguments de l'url et les insère dans un dictionnaire
        query = dict(urllib.parse.parse_qsl(parsed.query)) 
        # récupère la valeur de l'argument "filename" dans le dictionnaire
        filename = query.get("filename", "index.html")

        try:
            filename = os.path.join(BASE_DIR,query.get("filename"))
            print(filename)
        except:
            filename = os.path.join(BASE_DIR,"index.html")
        
        try:
            # essaie d'ouvrir le fichier spécifié par l'argument "filename"
            file = open(filename)
            print("ok")
        except:
            # si le fichier n'existe pas, ouvre index.html
            file = open(index_page) 
        finally:
            # lit le contenu du fichier, le convertit en bytes et l'écrit dans wfile pour l'envoyer au client
            self.wfile.write(bytes(file.read(), "utf-8"))
            print("ok2")



Server = HTTPServer((HOST, PORT), WebServer)
# Ouvre le navigateur vers l'adresse du serveur 
# (note: le préfixe "http://" n'est pas nécessaire dans la situation d'une adresse IP)
if os.environ.get("OPEN_BROWSER") == "1":
    webbrowser.open("http://localhost:" + str(PORT))

print("server running")
# Démarre le serveur HTTP et attend les requêtes entrantes en boucle
Server.serve_forever()