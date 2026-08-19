PORT = 8080


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

class XSS_web_server(BaseHTTPRequestHandler):

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
            print(message)
            html += "<h1>"+message+"</h1>"
        except:
            pass
        self.send_response(200)
        self.end_headers()
        html += "</body>"
        self.wfile.write(html.encode())


server = HTTPServer((HOST,PORT), XSS_web_server)
webbrowser.open(HOST + ":" + str(PORT))
print("server running")
server.serve_forever()
