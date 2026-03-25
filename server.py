from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib

PORT = 8080
HOST = "localhost"

class Web_Server_TM(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)  #sends back ok response
        self.send_header("content-type", "text/html")
        self.end_headers()
        
        parsed = urllib.parse.urlparse(self.path)
        print(parsed)
        #parameters =
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