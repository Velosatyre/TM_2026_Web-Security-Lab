"""
Ce type de vulnérabilité n'est pas traité dans le TM.
Ce serveur n'est qu'un bonus qui, pour manque de temps, n'a pas été intégré dans le TM.

Ce serveur donne la possibilité d'afficher du texte de la même manière que les sites
comme X(Twitter). 
La subtilité est que le texte n'est pas contrôler.
Une page html affiche le texte comme un paragraphe. 
Cela signifie qu'il est possible d'ajouter du code html ou JavaScript et il sera affiché sur le site.

Cette vulnérabilité s'appelle le Cross-Site Scripting (XSS).
"""

import socket,urllib,webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

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

class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET affiche sur la page web le message reçu.
    """

    def do_GET(self):
        html = """
        <body>
        <form>
            <label for="message">Message</label><br>
            <input type="text" id="message" name="message">
        </form>
        """

        parsed = urllib.parse.urlparse(self.path)
        query = dict(urllib.parse.parse_qsl(parsed.query))

        try:
            message = query["message"]
            html += "<h1>"+message+"</h1>"

        except:

            pass

        self.send_response(200)
        self.end_headers()

        html += "</body>"
        self.wfile.write(html.encode())


Server = HTTPServer((HOST, PORT), WebServer)
# Ouvre le navigateur vers l'adresse du serveur
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
Server.serve_forever()