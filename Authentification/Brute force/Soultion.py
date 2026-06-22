from http.server import BaseHTTPRequestHandler,HTTPServer
import os,socket,urllib

PORT =  8080
def IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    IP = s.getsockname()[0]
    return IP

HOST = IP()
print(HOST+":"+str(PORT))
usernames = ["admin"]
credentials = {
    "admin":"admin"
}

IPs = {

}

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "home.html"))
psswd = os.path.abspath(os.path.join(BASE_DIR, "home_err_psswd.html"))
usr = os.path.abspath(os.path.join(BASE_DIR, "home_err_usr.html"))
logged = os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))



class web_server(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.client_address[0])
        self.send_response(200)
        self.end_headers()
        file = open(home_page)
        self.wfile.write(bytes(file.read(),"utf-8"))
    
    def do_POST(self):
        IP = str(self.client_address[0])
        if IP in IPs and IPs[IP] > 5:
            self.send_error(401,"Your IP has been banned")
            return
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        query = dict(urllib.parse.parse_qsl(body.decode()))
        password = query["password"]
        username = query["username"]
        if username not in usernames:
            self.send_response(401,"Wrong username")
            self.end_headers()
            file = open(usr)
            self.wfile.write(bytes(file.read(),"utf-8"))
            try:
                number = IPs[IP]
                IPs.update({IP:number+1})
            except:
                IPs[IP] = 1
            return
        else:
            if password == credentials[username]:
                self.send_response(200)
                self.end_headers()
                file = open(logged)
                self.wfile.write(bytes(file.read(),"utf-8"))
                return
            else:
                self.send_response(401,"Wrong password")
                self.end_headers()
                file = open(psswd)
                self.wfile.write(bytes(file.read(),"utf-8"))
                try:
                    number = IPs[IP]
                    IPs.update({IP:number+1})
                except:
                    IPs[IP] = 1
                return


server = HTTPServer((HOST, PORT), web_server)
server.serve_forever() 