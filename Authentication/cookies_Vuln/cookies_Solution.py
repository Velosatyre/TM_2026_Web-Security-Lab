"""
Afin de contrôler si un cookie a été changé, l'idée est de faire un hash du cookie qui est envoyé.
Quand le client fera une requête, le serveur va alors hasher le coookie qu'il reçoit
et le comparer au sien.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os, urllib, secrets


PORT = 8080
HOST = "localhost"

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
home_page_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))
home_page_exp = os.path.abspath(os.path.join(BASE_DIR, "home_exp.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))

SESSION_ID = {

}

Users = {
    "admin":"admin",
    "alice":"123",
    "test":"test"
}

def SSID_Generator():
    SSID = secrets.token_urlsafe(16)
    return SSID

class Web_Server_TM(BaseHTTPRequestHandler):

    def do_GET(self):
        cookies = SimpleCookie(self.headers.get("Cookie"))
        file = home_page
        

        # analyse syntaxique de l'url
        parsed = urllib.parse.urlparse(self.path)
        # récupère uniquement les arguments de l'url et les insère dans un dictionnaire
        query = dict(urllib.parse.parse_qsl(parsed.query))
        if "SSID" in cookies:
            if cookies["SSID"].value in SESSION_ID:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                file = logged_in_page
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                file = home_page_err

        elif "SSID" not in cookies:
            try:
                if query["user"] in Users and query["pass"] == Users[query["user"]]:
                    SSID = SSID_Generator()
                    SESSION_ID[SSID] = query["user"]
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Set-Cookie", f"SSID={SSID} ; max-age=60")
                    self.end_headers()
                    file = logged_in_page
                else:
                    file = home_page_err
                    self.send_response(401)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
            except:
                file = home_page
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
        

        files = open(file)
        self.wfile.write(bytes(files.read(), "utf-8"))

        


server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")