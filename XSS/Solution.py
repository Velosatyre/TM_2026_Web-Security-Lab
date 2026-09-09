"""
La solution ici est tout d'abord d'encoder le message reçu.
Quand le navigateur web reçoit la page html, le message sera interprété comme du texte et non comme du code html ou JavaScript.
"""

import socket,urllib,html,os
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

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")

class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET filtre le message reçu, les caractères spéciaux sont encodés
      pour éviter l'affichage de code HTML ou JavaScript.
    """

    def do_GET(self):
        html_page = """
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

            # This converts < to &lt;, > to &gt;, & to &amp;, " to &quot;, ' to &#x27;
            escaped_message = html.escape(message)
            html_page += "<h1>"+escaped_message+"</h1>"

        except:

            pass

        self.send_response(200)
        self.end_headers()

        html_page += "</body>"
        self.wfile.write(html_page.encode())


Server = HTTPServer((HOST, PORT), WebServer)

Server.serve_forever()
