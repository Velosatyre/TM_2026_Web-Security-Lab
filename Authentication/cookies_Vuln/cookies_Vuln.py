"""
Voici un exemple dimplementation des cookies sans aucune securite
Le cookie est la variable logged_in qui represente si lutilisateur est
connecte. Pour ce connecter sans code il suffit dinspecter la page, et aller dans storage.
La bas il y aura le cookie. Il faut juste changer la valeur de False a True.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os


PORT = 8080
HOST = "localhost"
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))


class Web_Server_TM(BaseHTTPRequestHandler):

    def do_GET(self):
        cookies = SimpleCookie(self.headers.get("Cookie"))
        print(cookies)
        file = home_page
        if "logged_in" in cookies:
            logged_in_cookie = cookies["logged_in"].value
        print(logged_in_cookie)

        if logged_in_cookie == "True":
            file = logged_in_page

        elif logged_in_cookie == "False":
            file = home_page

        self.send_response(200)
        self.send_header("content-type", "text/html")
        if not "logged_in" in cookies:
            self.send_header("Set-Cookie", "logged_in=False")
        self.end_headers()
        files = open(file)
        self.wfile.write(bytes(files.read(), "utf-8"))

        


server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")