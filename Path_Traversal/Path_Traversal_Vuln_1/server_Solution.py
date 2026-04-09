from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
import os
"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'acceder à des fichiers hors du serveur comme par exemple
etc/passwd

Voici comment y remedier (Mon idée):
Il est possible ce creer une liste de paths que les serveur peut accéder
et bloquer s'il essaye d'en accéder une autre. Malheureseument cette technique prend beacoup
de temps si le site contient beacoup de fichiers mais cette technique bloque toute possibilié de Path Traversal



"""

PORT = 8080
HOST = "localhost"
Authorized_paths = ["/","","Path_Traversal_Vuln_1/login.html","Path_Traversal_Vuln_1/index.html"]

class Web_Server_TM_Netcat_V1(BaseHTTPRequestHandler):

    def do_GET(self):
        a=0
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "text/html")
        self.end_headers()
        
        parsed = urllib.parse.urlparse(self.path)       #gets args of the url
        path = parsed.path                              #gets only path in the url
        #path = path[1:]                                #removes the default / that is necessary in the url
        print(path)
        path = os.path.abspath(path)
        print(path)
        try :
            for i in Authorized_paths:
                if path == i:
                    a += 1
            if a ==0:
                self.send_error(418)                #couldn't find a precise error code so Aprilfool's one the best
            else:
                file = open(path)                           #opens file in the path
        except:
            file = open("index.html")
        finally:
            self.wfile.write(bytes(file.read(), "utf-8"))   #reads the file, transform into bytes and writes it into wfile to send it to reciever

class Web_Server_TM_Web_browser_V1(BaseHTTPRequestHandler):

    def do_GET(self):
        a=0
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "text/html")
        self.end_headers()
        
        parsed = urllib.parse.urlparse(self.path)       #gets info from the url
        query = dict(urllib.parse.parse_qsl(parsed.query))
        print(query)
        filename = query.get("filename")
        print(filename)
        filename = os.path.abspath(filename)
        print(filename)
        try :
            for i in Authorized_paths:
                if filename == i:
                    a += 1
            if a ==0:
                self.send_error(418)                #couldn't find a precise error code so Aprilfool's one the best
            else:
                file = open(filename)                           #opens file in the path
        except:
            file = open("index.html")
        finally:
            self.wfile.write(bytes(file.read(), "utf-8"))   #reads the file, transform into bytes and writes it into wfile to send it to reciever

        
       



server = HTTPServer((HOST,PORT), Web_Server_TM_Web_browser_V1)
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")