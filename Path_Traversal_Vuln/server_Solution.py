from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'acceder à des fichiers hors du serveur comme par exemple
etc/passwd

Voici comment y remedier (Mon idée):
Il est possible ce creer une liste de paths que les serveur peut accéder
et bloquer s'il essaye d'en accéder une autre. Possible uniquement si peu de sites annexes sinon cela prend trop de temps

Solution la plus commune sur internet :

"""

PORT = 8080
HOST = "localhost"
Authorized_paths = ["/","","Path_Traversal_Vuln/login.html","Path_Traversal_Vuln/index.html"]

class Web_Server_TM_Netcat_V1(BaseHTTPRequestHandler):

    def do_GET(self):
        a=0
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "text/html")
        self.end_headers()
        
        parsed = urllib.parse.urlparse(self.path)       #gets args of the url
        path = parsed.path                              #gets only path in the url
        path = path[1:]                                #adds . to path so it works locally
        try :
            for i in Authorized_paths:
                if path == i:
                    a += 1
            if a ==0:
                self.send_error(418)                #couldn't find a precise error code so Aprilfool's one the best
            else:
                file = open(path)                           #opens file in the path
        except:
            file = open("Path_Traversal_Vuln/index.html")
        finally:
            self.wfile.write(bytes(file.read(), "utf-8"))   #reads the file, transform into bytes and writes it into wfile to send it to reciever




server = HTTPServer((HOST,PORT), Web_Server_TM_Netcat_V1)
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")