"""
Solution très simple, il suffit de faire un check juste avant en regardant si la catégorie reçue 
est bien dans la liste des catégories de la base de données.
"""

import os,urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from SQL_fetch import FETCH_SQL

PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")

BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))
logged_in= os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))
home_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))

with open('/app/log/SQL_requests.log', 'w'):
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


        # Génération de la page html, aidé par Copilot de VS code, le 16.6.2026
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

Server.serve_forever()