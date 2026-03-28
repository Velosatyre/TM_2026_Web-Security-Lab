from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'acceder à des fichiers hors du serveur comme par exemple
etc/passwd
Comment :
    Terminal:
        nc localhost 8080  #cela lance netcat et dit d'envoyer des requêtes à localhost sur le port 8080
        GET /../../../etc/passwd HTTP/1.1   #il faut écrire à la main la requête

        curl http://localhost:8080/Path_Traversal_Vuln/login.html?filename=../../../etc/passwd
    Web browser:
        Il faut click sur login, ensuite dans l'url il faut remplacer ce qu'il y a après filname=
        avec ../../../etc/passwd
        http://localhost:8080/Path_Traversal_Vuln/login.html?filename=../../../etc/passwd
    

"""

PORT = 8080
HOST = "localhost"

class Web_Server_TM_Netcat_V1(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "text/html")
        self.end_headers()
        
        parsed = urllib.parse.urlparse(self.path)       #gets info from the url
        path = parsed.path                              #gets only path in the url
        path = path[1:]                                #removes the first char of the string which is /
        print(path)
        try :
            file = open(path)                           #opens file in the path
        except:
            file = open("Path_Traversal_Vuln/index.html")
        finally:
            self.wfile.write(bytes(file.read(), "utf-8"))   #reads the file, transform into bytes and writes it into wfile to send it to reciever


class Web_Server_TM_Web_browser_V1(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "text/html")
        self.end_headers()
        
        parsed = urllib.parse.urlparse(self.path)       #gets info from the url
        query = dict(urllib.parse.parse_qsl(parsed.query))
        print(query)
        filename = query.get("filename")
        print(filename)
        try :
            file = open(filename)                           #opens file in the path
        except:
            file = open("Path_Traversal_Vuln/index.html")
        finally:
            self.wfile.write(bytes(file.read(), "utf-8"))   #reads the file, transform into bytes and writes it into wfile to send it to reciever

        
       





#server = HTTPServer((HOST,PORT), Web_Server_TM_Netcat_V1)  #if you use netcat
server = HTTPServer((HOST,PORT), Web_Server_TM_Web_browser_V1) #if you use web browser or curl
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")