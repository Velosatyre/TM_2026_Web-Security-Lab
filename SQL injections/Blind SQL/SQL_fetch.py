import psycopg
import logging
import time
import subprocess as sub
logger = logging.getLogger(__name__)
logging.basicConfig(filename='SQL_requests.log', level=logging.INFO)
"""
Afin de créer une base de données pour la première fois que vous utilisez Postgresql.
Il vous faudra executer quelques commandes dans le Terminal.
L'auteur de ce programme ne prend aucune responsabilité sur le résultat d'execution du code.
Linux :

$ whoami
# Cela va vous fournir votre nom d'utilisateur

$ sudo -u postgres psql -c create database tm_db;

$ sudo -u postgres psql -d tm_db -c grant all on table to #mettez votre nom d'utilisateur ici#;

$ sudo -u postgres psql -d tm_db -c grant all on schema public to #nom d'utilisateur#;
"""


def FETCH_SQL(sql_query, params=None): # params handling made by AI
    with psycopg.connect("dbname=tm_db") as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            try :
                if params is None:
                    cur.execute(sql_query)
                    logger.info(time.asctime(time.gmtime())+f" : Executed SQL query: {sql_query}")
                else:
                    # Normalize single non-sequence param (e.g. a string) to a tuple
                    if not isinstance(params, (list, tuple, dict)):
                        exec_params = (params,)
                    else:
                        exec_params = params
                    cur.execute(sql_query, exec_params)
                    logger.info(time.asctime(time.gmtime())+f" : Executed SQL query: {sql_query} with params: {exec_params}")

                response = cur.fetchall()
                logger.info(time.asctime(time.gmtime())+f" : Fetched data: {response}")
                return response
            except Exception as e:
                logger.error(time.asctime(time.gmtime())+" : "+str(e))
                return []
            

