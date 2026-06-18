PORT = 8080


import socket,urllib,html
from http.server import BaseHTTPRequestHandler, HTTPServer

def IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    IP = s.getsockname()[0]
    return IP

HOST = IP()
print(HOST+":"+str(PORT))

class XSS_web_server(BaseHTTPRequestHandler):

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
            print(message)
            # This converts < to &lt;, > to &gt;, & to &amp;, " to &quot;, ' to &#x27;
            escaped_message = html.escape(message)
            html_page += "<h1>"+escaped_message+"</h1>"
        except:
            pass
        self.send_response(200)
        self.end_headers()
        html_page += "</body>"
        self.wfile.write(html_page.encode())


server = HTTPServer((HOST,PORT), XSS_web_server) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")
