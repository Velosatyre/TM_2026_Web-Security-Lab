import os
import psycopg
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(filename='SQL_requests.log', level=logging.INFO)

def FETCH_SQL(sql_query, params=None): # params handling made by Copilot from VS code
    """
    https://www.psycopg.org/psycopg3/docs/basic/usage.html
    Cette fonction a pour but d'envoyer les requêtes SQL à la base de données.
    Au passage elle crée un historique des requêtes dans le fichier SQL_requests.log
    """
    with psycopg.connect(os.environ.get("DATABASE_URL", "dbname=tm_db")) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            try :
                if params is None:
                    cur.execute(sql_query)
                    logger.info(time.asctime(time.gmtime())+f" : Executed SQL query: {sql_query}")
                else:
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
