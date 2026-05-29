import psycopg
import logging
import time
logger = logging.getLogger(__name__)
logging.basicConfig(filename='SQL_requests.log', level=logging.INFO)

def FETCH_SQL(sql_query):
    with psycopg.connect("dbname=test_db user=artur") as conn:
        with conn.cursor() as cur:
            try :
                cur.execute(sql_query)
                logger.info(time.asctime(time.gmtime())+f" : Executed SQL query: {sql_query}")
                response = cur.fetchall()
                logger.info(time.asctime(time.gmtime())+f" : Fetched data: {response}")
                return response
            except Exception as e:
                logger.error(time.asctime(time.gmtime())+" : "+str(e))
            
    conn.commit()


    