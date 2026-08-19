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


usernames = ["admin"]
credentials = {
    "admin": "admin"
}

# Dictionnaire IP 
IPs = {}


# Chemins vers les pages HTML utilisées
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
psswd = os.path.abspath(os.path.join(BASE_DIR, "home_err_psswd.html"))
usr = os.path.abspath(os.path.join(BASE_DIR, "home_err_usr.html"))
logged = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))


class web_server(BaseHTTPRequestHandler):

    def do_GET(self):
        # Log l'adresse cliente puis servir la page d'accueil
        print(self.client_address[0])
        self.send_response(200)
        self.end_headers()
        file = open(home_page)
        self.wfile.write(bytes(file.read(), "utf-8"))

    def do_POST(self):
        # Adresse IP du client
        IP = str(self.client_address[0])

        # Vérifier si l'IP est bannie (ici après > 5 échecs)
        if IP in IPs and IPs[IP] > 5:
            # Répondre avec une erreur 401
            self.send_error(401, "Your IP has been banned")
            return

        # Lire le corps de la requête POST
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        query = dict(urllib.parse.parse_qsl(body.decode()))

        # Extraire les champs attendus
        password = query["password"]
        username = query["username"]

        # Nom d'utilisateur inconnu
        if username not in usernames:
            self.send_response(401, "Wrong username")
            self.end_headers()
            file = open(usr)
            self.wfile.write(bytes(file.read(), "utf-8"))
            # Incrémenter le compteur d'échecs pour cette IP
            try:
                number = IPs[IP]
                IPs.update({IP: number + 1})
            except:
                IPs[IP] = 1
            return
        else:
            # Vérifier le mot de passe
            if password == credentials[username]:
                self.send_response(200)
                self.end_headers()
                file = open(logged)
                self.wfile.write(bytes(file.read(), "utf-8"))
                return
            else:
                # Mauvais mot de passe : incrément du compteur et page d'erreur
                self.send_response(401, "Wrong password")
                self.end_headers()
                file = open(psswd)
                self.wfile.write(bytes(file.read(), "utf-8"))
                try:
                    number = IPs[IP]
                    IPs.update({IP: number + 1})
                except:
                    IPs[IP] = 1
                return


server = HTTPServer((HOST, PORT), web_server)
# Ouvre le navigateur vers l'adresse du serveur 
#(note: le préfixe "http://" n'est pas nécessaire dans la situation d'une adresse IP)
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
# Démarre le serveur HTTP et attend les requêtes entrantes en boucle
server.serve_forever()