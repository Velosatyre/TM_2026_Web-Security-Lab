from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
"""
Première faille, path traversal
Il est possible en envoyant une requête au serveur
d'acceder à des fichiers hors du serveur comme par exemple
etc/passwd
Comment :
    Terminal(linux):
        nc localhost 8080
        GET ./../../etc/passwd HTTP/1.1
    Web browser:
        pas possible pour l'instant


"""

PORT = 8080
HOST = "localhost"

class Web_Server_TM(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "text/html")
        self.end_headers()
        
        parsed = urllib.parse.urlparse(self.path)       #gets args of the url
        path = parsed.path                              #gets only path in the url
        path = "."+path                                 #adds . to path so it works locally
        print(path)
        
        try :
            file = open(path)                           #opens file in the path
        except:
            file = open("index.html")
        finally:
            self.wfile.write(bytes(file.read(), "utf-8"))   #reads the file, transform into bytes and writes it into wfile to send it to reciever

        #self.wfile.write(bytes("<html><body><h1>HELLO WOLRD</h1></body></html>", "utf-8"))
        

    def do_POST(self):
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "application/json")
        self.end_headers()

        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes('{"time": "' + date + '"}', "utf-8"))



server = HTTPServer((HOST,PORT), Web_Server_TM)
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")