"""
Serveur qui ne contrôle pas les tentatives de connexion.
Il est donc vulnérable aux attaques par force brute.
"""

from http.server import BaseHTTPRequestHandler,HTTPServer
import os,urllib

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")
print(HOST+":"+str(PORT))

#informations des utilisateurs
usernames = ["admin"]
credentials = {
    "admin": "admin"
}


# Chemins absolus vers les fichiers HTML utilisés
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
wrong_password = os.path.abspath(os.path.join(BASE_DIR, "wrong_password.html"))
wrong_username = os.path.abspath(os.path.join(BASE_DIR, "wrong_username.html"))
logged = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))


class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET sert la page d'accueil ('home_page').
    
    - do_POST lit le corps de la requête POST, 
      en extrait 'username' et 'password', 
      puis compare ces valeurs avec sa base de données 
      (ici, le dictionnaire 'credentials').
    """

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        
        file = open(home_page)
        self.wfile.write(bytes(file.read(), "utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        query = dict(urllib.parse.parse_qsl(body.decode()))

        password = query["password"]
        username = query["username"]

        if username not in usernames:

            self.send_response(401, "Wrong username")
            self.end_headers()

            file = open(wrong_username)
            self.wfile.write(bytes(file.read(), "utf-8"))
            return
        
        else:
            
            if password == credentials[username]:
                
                self.send_response(200)
                self.end_headers()

                file = open(logged)
                self.wfile.write(bytes(file.read(), "utf-8"))
                return
            
            else:
                
                self.send_response(401, "Wrong password")
                self.end_headers()
                
                file = open(wrong_password)
                self.wfile.write(bytes(file.read(), "utf-8"))
                return


Server = HTTPServer((HOST, PORT), WebServer)

Server.serve_forever()