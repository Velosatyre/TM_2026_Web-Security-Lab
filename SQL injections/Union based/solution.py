"""
Solution très simple, il suffit de faire un check juste avant en regardant si la catégorie reçue 
est bien dans la liste des catégories de la base de données.
"""

import os,urllib,socket, webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from SQL_fetch import FETCH_SQL

def IP():
# Source - https://stackoverflow.com/a/166589
# Posted by UnkwnTech, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-17, License - CC BY-SA 3.0
    """
    Retourne l'adresse IP locale de la machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

PORT =  8080
HOST = IP()
print("adresse du serveur: " + HOST + ":" + str(PORT))

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))
logged_in= os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))
home_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))

with open('SQL_requests.log', 'w'):
    pass

class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET compare la catégorie reçue avec celles de la base de données, 
      si elle n'est pas dans la liste, le serveur renvoie tous les produits.
      La page html est générée dynamiquement en fonction de la catégorie reçue.
    """

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        category = None

        if query.startswith("category="):
            category = query.split("=")[1]
            category = urllib.parse.unquote(category)
            
        listed_categories = [cat[0] for cat in FETCH_SQL("SELECT DISTINCT category FROM products where released = TRUE ORDER BY category")]
        
        if category in listed_categories:
            products = FETCH_SQL("SELECT name, price FROM products where released = TRUE and category = '" + category + "'")
        else:
            products = FETCH_SQL("SELECT name, price FROM products where released = TRUE")


        # aidé par l'IA
        html = """
        </head>
        <body>

        <h1>My Shop</h1>

        <div class="filters">
            <a href="/"><button>All</button></a>
        """

        for cat in listed_categories:
            html += f"""
            <a href="/?category={cat}">
                <button>{cat}</button>
            </a>
            """

        html += "</div>"

        for name, price in products:
            html += f"""
            <div class="product">
                <h3>{name}</h3>
                <p>CHF {price}</p>
            </div>
            """

        html += """
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(html.encode())

Server = HTTPServer((HOST, PORT), WebServer)
# Ouvre le navigateur vers l'adresse du serveur
webbrowser.open(HOST + ":" + str(PORT))

print("server running")
Server.serve_forever()