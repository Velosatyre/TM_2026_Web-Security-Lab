"""
Les attaques par injection sql laissent la possibilité de récupérer des données qui ne sont pas censées être vues.
Ici il est possible de voir le résultat de la requête SQl,
Ce qui permet d'utiliser les injections utilisant UNION pour récupérer des données de la base de données.
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

with open('SQL_requests.log', 'w'):
    pass

class WebServer(BaseHTTPRequestHandler):
    """
    - do_GET prend la catégorie reçue, 
      va chercher er dans la base de données tout les produits de cette catégorie et les affiche.
      Si la catégorie n'est pas dans la base de données, le serveur renvoie tous les produits.
    """

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        category = None

        if query.startswith("category="):
            category = query.split("category=")[1]
            category = urllib.parse.unquote(category)
        
        categories_grp = FETCH_SQL("SELECT DISTINCT category FROM products where released = TRUE ORDER BY category")
        categories = [cat[0] for cat in categories_grp]
        
        if category:
            products = FETCH_SQL("SELECT name, price FROM products where released = TRUE and category = '" + category + "'")

        else:
            products = FETCH_SQL("SELECT name, price FROM products where released = TRUE")


        # aidé par Copilot de VS code
        html = """
        </head>
        <body>

        <h1>My Shop</h1>

        <div class="filters">
            <a href="/"><button>All</button></a>
        """

        for cat in categories:
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