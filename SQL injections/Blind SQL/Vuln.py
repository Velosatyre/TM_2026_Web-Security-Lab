"""
Pour cette vulnérabilité il faudra utiliser burpsuite community afin d'automatiser les attaques
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import os,secrets
from SQL_fetch import FETCH_SQL


PORT = 8080
HOST = "192.168.1.41"

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
logged_in_page = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))
FETCH_SQL("delete from sessions;")
FETCH_SQL("create table if not exists sessions (SSID varchar(255));")
with open('SQL_requests.log', 'w'):
    pass
def SSID_Generator():
    SSID = secrets.token_urlsafe(16)
    return SSID

class Web_Server_TM(BaseHTTPRequestHandler):

    def do_GET(self):
        cookies = SimpleCookie(self.headers.get("Cookie"))
        if not "SSID" in cookies:
            print("no cookie")
            SSID = SSID_Generator()
            self.send_response(200)
            self.send_header("Set-Cookie", f"SSID={SSID};")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open(home_page)
            html = file.read().format(message="WELCOME")
            FETCH_SQL("insert into sessions (SSID) values ('" + SSID + "');")
            print("done")
        else:
            SSID = cookies["SSID"].value
            print(SSID)
            sessions = FETCH_SQL("select * from sessions where SSID = '" + SSID + "';")
            print(sessions)
            if sessions == None:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                file = open(home_page)
                html = file.read().format(message="WELCOME")
            elif len(sessions) > 0:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                file = open(home_page)
                html = file.read().format(message="WELCOME BACK")
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                file = open(home_page)
                html = file.read().format(message="WELCOME")

        self.wfile.write(bytes(html, "utf-8"))  
        


server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")