"""
Protection contre les attaques par force brute.
Le serveur bloque l'adresse IP après 5 tentatives de connexion échouées.
"""

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

# informations des utilisateurs
usernames = ["admin"]
credentials = {
    "admin": "admin"
}

# Dictionnaire des IP bannies
IPs = {}


# Chemins vers les pages HTML utilisées
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
wrong_password = os.path.abspath(os.path.join(BASE_DIR, "wrong_password.html"))
wrong_username = os.path.abspath(os.path.join(BASE_DIR, "wrong_username.html"))
logged = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))


class WebServer(BaseHTTPRequestHandler):

    """
    - do_GET sert la page d'accueil ('home_page').
    
    - do_POST fait la même chose que dans la version vulnérable, 
      mais enregistre les tentatives de connexion échouées 
      et bloque l'adresse IP après 5 échecs.
    """
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        
        file = open(home_page)
        self.wfile.write(bytes(file.read(), "utf-8"))

    def do_POST(self):
        IP = str(self.client_address[0])

        if IP in IPs and IPs[IP] > 5:
            self.send_error(401, "Your IP has been banned")
            return

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

                try:
                    number = IPs[IP]
                    IPs.update({IP: number + 1})
                
                except:
                    IPs[IP] = 1

                return


Server = HTTPServer((HOST, PORT), WebServer)
# Ouvre le navigateur vers l'adresse du serveur 
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
Server.serve_forever()