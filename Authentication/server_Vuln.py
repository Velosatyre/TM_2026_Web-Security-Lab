from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
import os

PORT = 8080
HOST = "localhost"

Usernames = {
    0: "admin",
    1: "alice",
    2: "bob"
}
Passwords = {
    0:"admin",
    1:"123",
    2:"test"
}

class Web_Server_TM(BaseHTTPRequestHandler):

    def do_GET(self):
        a = False
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "text/html")
        self.end_headers()

        parsed = urllib.parse.urlparse(self.path)       #gets info from the url
        query = dict(urllib.parse.parse_qsl(parsed.query))  #gets the args of the url, everything after the question mark ?
        print(query)
        if len(query) != 0:
            for i in Usernames:
                if query["user"] == Usernames[i] and query["pass"] == Passwords[i]:
                    file = open("Authentication/logged_in.html")
                    a = True
            if a == False:
                self.send_error(401)
        else:
            file = open("Authentication/index.html")


            
        self.wfile.write(bytes(file.read(), "utf-8"))   #sends default webpage to user

server = HTTPServer((HOST,PORT), Web_Server_TM) 
print("server running")
server.serve_forever()
server.server_close()
print("server stopped")