PORT = 8080
HOST = "192.168.1.41"

import socket,urllib
from http.server import BaseHTTPRequestHandler, HTTPServer

def IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    IP = s.getsockname()[0]
    return IP

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
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")
