"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'accéder à des fichiers hors du serveur comme par exemple
etc/passwd

Comment :
    Web browser:
        Il faut appuyer sur login, ensuite dans l'url il faut remplacer ce qu'il y a après filename=
        avec ../../../../etc/passwd
        http://localhost:8080/login.html?filename=../../../../etc/passwd
Explication :
    Dans une base de données ../ signifie de remonter d'une directory; User:~/dossier/dossier$ cd ../ -> User:~/dossier$
    Donc quand dans l'url on écrit ../../../etc/passwd, le serveur, pour aller chercher les fichier, il va remonter trois fois 
    puis va entrer dans le dossier /etc pour ouvrir le fichier passwd -> cette manipulation marche uniquement si le serveur se trouve au troisième "étage".

    P.S le nombre de fois qu'il faut mettre ../ est équivalant à la quantité de dossiers dont il doit sortir pour arriver dans le root.
    Dans mon cas c'est 4 fois mais cela peut varier en fonction de où vous avez placé ces fichiers.

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
        try:
            filename = os.path.join(BASE_DIR,query.get("filename"))
        except:
            filename = os.path.join(BASE_DIR,"index.html")

        try:
            # essaie d'ouvrir le fichier spécifié par l'argument "filename"
            file = open(filename) 
        except:
            # si le fichier n'existe pas, ouvre index.html
            file = open(index_page) 
        finally:
            # lit le contenu du fichier, le convertit en bytes et l'écrit dans wfile pour l'envoyer au client
            self.wfile.write(bytes(file.read(), "utf-8")) 



Server = HTTPServer((HOST, PORT), WebServer)
# Ouvre le navigateur vers l'adresse du serveur 
# (note: le préfixe "http://" n'est pas nécessaire dans la situation d'une adresse IP)
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
# Démarre le serveur HTTP et attend les requêtes entrantes en boucle
Server.serve_forever()