"""
Les attaques par injection sql laissent la possibilité de récupérer des données qui ne sont pas censées être vues.
Dans cet exercices il y a quelques étapes à effectuer afin de tout récuperer.
Tout d'abord
"""


import os,urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import SQL_fetch
from SQL_fetch import FETCH_SQL
import subprocess as sub

PORT = 8080
HOST = "localhost"
BASE_DIR = os.path.dirname(__file__)
home_page = os.path.abspath(os.path.join(BASE_DIR, "login.html"))
logged_in= os.path.abspath(os.path.join(BASE_DIR, "logged_in.html"))
home_err = os.path.abspath(os.path.join(BASE_DIR, "home_err.html"))
with open('SQL_requests.log', 'w'):
    pass

class Shop(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        print(query)
        category = None
        if query.startswith("category="):
            category = query.split("=")[1]
            category = urllib.parse.unquote(category)
        print(category)
        
        categories_grp = FETCH_SQL("SELECT DISTINCT category FROM products where released = TRUE ORDER BY category;")
        categories = [cat[0] for cat in categories_grp]
        print(categories)
        if category:
            products = FETCH_SQL("SELECT name, price FROM products where released = TRUE and category = '" + category + "';")
        else:
            products = FETCH_SQL("SELECT name, price FROM products where released = TRUE;")



        # AI powered HTML generation
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

server = HTTPServer(("localhost", 8080), Shop)

print("Server running")
server.serve_forever()