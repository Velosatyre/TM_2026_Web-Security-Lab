"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'acceder à des fichiers hors du serveur comme par exemple
etc/passwd

Comment :
    Terminal:
        nc localhost 8080  #cela lance netcat et dit d'envoyer des requêtes à localhost sur le port 8080
        GET /../../../../etc/passwd HTTP/1.1   #il faut écrire à la main la requête

        curl http://localhost:8080/login.html?filename=../../../../etc/passwd
    Web browser:
        Il faut appuyer sur login, ensuite dans l'url il faut remplacer ce qu'il y a après filname=
        avec ../../../etc/passwd
        http://localhost:8080/login.html?filename=../../../../etc/passwd
Expliquation :
    Dans une base de données ../ signifie de remonter d'une directory; User:~/dossier/dossier$ cd ../ -> User:~/dossier$
    Donc quand dans l'url on écrit ../../../etc/passwd, le serveur, pour aller chercher les fichier, il va remonter trois fois 
    puis va entrer dans le dossier /etc pour ouvrir le fichier passwd -> cette manipulation marche uniquement si le serveur se trouve au troisième "étage".

    P.S le nobre de fois qu'il faut mettre ../ est equivalant à la quantité de dossiers dont il doit sortir pour arriver dans le root.
    Dans mon cas c'est 4 fois mais cela peut varier en fonction de où vous avez placé ces fichiers.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

PORT = 8080
HOST = "localhost"


class Web_Server_TM_Netcat_V1(BaseHTTPRequestHandler): #version pour netcat
    def do_GET(self):
        self.send_response(200) # envoie une réponse 200 (ok)
        self.send_header("content-type", "text/html") # envoi un header avec comme variable en plus le content-type qui est du html
        self.end_headers()

        parsed = urllib.parse.urlparse(self.path) # analyse syntaxique de l'url
        path = parsed.path # récupère uniquement le path de l'url
        path = path[1:]  # enlève le / du début
        #print(path)

        try:
            file = open(path) # essaie d'ouvrir le fichier dans le path
        except:
            file = open("./index.html") # si le fichier n'existe pas, ouvre index.html
        finally:
            self.wfile.write(bytes(file.read(), "utf-8")) # lit le contenu du fichier, le convertit en bytes et l'écrit dans wfile pour l'envoyer au client


class Web_Server_TM_Web_browser_V1(BaseHTTPRequestHandler): # version pour navigateur web ou curl
    def do_GET(self):
        self.send_response(200) # envoie une réponse 200 (ok)
        self.send_header("content-type", "text/html") # envoi un header avec comme variable en plus le content-type qui est du html
        self.end_headers()

        parsed = urllib.parse.urlparse(self.path) # analyse syntaxique de l'url
        query = dict(urllib.parse.parse_qsl(parsed.query)) # récupère uniquement les arguments de l'url et les insère dans un dictionnaire
        print(query)
        filename = query.get("filename") # récupère la valeur de l'argument "filename" dans le dictionnaire

        try:
            print(filename)
            file = open(filename) # essaie d'ouvrir le fichier spécifié par l'argument "filename"
            print("ok")
        except:
            file = open("./index.html") # si le fichier n'existe pas, ouvre index.html
        finally:
            self.wfile.write(bytes(file.read(), "utf-8")) # lit le contenu du fichier, le convertit en bytes et l'écrit dans wfile pour l'envoyer au client


# server = HTTPServer((HOST, PORT), Web_Server_TM_Netcat_V1)  # netcat version
server = HTTPServer((HOST, PORT), Web_Server_TM_Web_browser_V1)  # nav. Web/curl version
print("server running")
server.serve_forever() # démarre le serveur et le fait tourner indéfiniment