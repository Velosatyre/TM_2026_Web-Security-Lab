"""
Protection contre les attaques par force brute.
La première idée était de bannir l'adresse IP de l'attaquant.

Cependant, bannir définitivement une IP après 5 échecs bloque tous les utilisateurs 
légitimes partageant une même adresse IP publique (WiFi d'école, réseau 
d'entreprise). De plus, un attaquant 
peut faire exprès de faire bannir l'IP d'un utilisateur cible.

Meilleures méthodes(selon Gemini):
- Verrouiller temporairement le compte toutes les 3 à 5 tentatives d'une manière exponentielle.
- Blocage combiné (IP + Nom d'utilisateur), Verrouiller le compte spécifique sur l'adresse IP plutôt que de bloquer toute l'adresse IP globale.
Bonus : ajouter un CAPTCHA après 3 tentatives. Cela va bloquer les scripts de brute force.
"""

from http.server import BaseHTTPRequestHandler,HTTPServer
import os,urllib

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")
print(HOST+":"+str(PORT))

# informations des utilisateurs
usernames = ["admin","bob"]
credentials = {
    "admin": "admin",
    "bob": "secret"
}

# Nombre de tentatives de connexion
Tries = {
}

# Les comptes bloqués
Banned = {

}


# Chemins vers les pages HTML utilisées
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
wrong_login = os.path.abspath(os.path.join(BASE_DIR, "wrong_login.html"))
logged = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))


class WebServer(BaseHTTPRequestHandler):

    """
    - do_GET sert la page d'accueil ('home_page').
    
    - do_POST fait la même chose que dans la version vulnérable, 
      mais après 5 tentative, la fonction va bloquer le compte avec l'adresse IP(blocage combiné).
    """
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        
        file = open(home_page)
        self.wfile.write(bytes(file.read(), "utf-8"))

    def do_POST(self):
        IP = str(self.client_address[0])

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        query = dict(urllib.parse.parse_qsl(body.decode()))
        
        try:
            password = query["password"]
            username = query["username"]
        except:
            self.send_response(401)
            self.end_headers()
        
            file = open(wrong_login)
            self.wfile.write(bytes(file.read(), "utf-8"))
            return

        tries_key = (IP, username)

        if IP not in Banned:
            if username in usernames:
                if password == credentials[username]:
                    self.send_response(200)
                    self.end_headers()

                    file = open(logged)
                    self.wfile.write(bytes(file.read(), "utf-8"))
                    return
                else:
                    if tries_key in Tries:
                        if Tries[tries_key] >= 4:
                            Banned[IP] = username
                            Tries[tries_key] = 0

                            self.send_error(401, "You have been banned")
                            return
                        else:
                            Tries[tries_key] += 1
                            self.send_response(401)
                            self.end_headers()
    
                            file = open(wrong_login)
                            self.wfile.write(bytes(file.read(), "utf-8"))
                    else:
                        Tries[tries_key] = 1

                        self.send_response(401)
                        self.end_headers()

                        file = open(wrong_login)
                        self.wfile.write(bytes(file.read(), "utf-8"))

            else:
                if tries_key in Tries:
                    if Tries[tries_key] >= 4:
                        Banned[IP] = username
                        Tries[tries_key] = 0
                
                        self.send_error(401, "You have been banned")
                        return
                    else:
                        Tries[tries_key] += 1
                        self.send_response(401)
                        self.end_headers()
                
                        file = open(wrong_login)
                        self.wfile.write(bytes(file.read(), "utf-8"))
                else:
                    Tries[tries_key] = 1
                
                    self.send_response(401)
                    self.end_headers()
                
                    file = open(wrong_login)
                    self.wfile.write(bytes(file.read(), "utf-8"))

        elif IP in Banned and Banned[IP] != username:

            if username in usernames:
                if password == credentials[username]:
                    self.send_response(200)
                    self.end_headers()

                    file = open(logged)
                    self.wfile.write(bytes(file.read(), "utf-8"))
                    return
                else:
                    if tries_key in Tries:
                        if Tries[tries_key] >= 4:
                            Banned[IP] = username
                            Tries[tries_key] = 0

                            self.send_error(401, "You have been banned")
                            return
                        else:
                            Tries[tries_key] += 1
                            self.send_response(401)
                            self.end_headers()
    
                            file = open(wrong_login)
                            self.wfile.write(bytes(file.read(), "utf-8"))
                    else:
                        Tries[tries_key] = 1

                        self.send_response(401)
                        self.end_headers()

                        file = open(wrong_login)
                        self.wfile.write(bytes(file.read(), "utf-8"))

            else:
                self.send_response(401)
                self.end_headers()
    
                file = open(wrong_login)
                self.wfile.write(bytes(file.read(), "utf-8"))

        else:
            self.send_response(401, "You are banned")
            self.end_headers()
            

Server = HTTPServer((HOST, PORT), WebServer)
Server.serve_forever()