import psycopg
import logging
import time
import subprocess as sub
logger = logging.getLogger(__name__)
logging.basicConfig(filename='SQL_requests.log', level=logging.INFO)
user = sub.run(["whoami"], capture_output=True, text=True).stdout.strip()
#sub.run(["sudo", "-u", "postgres", "psql", "-c", "CREATE DATABASE tm_db;"])
#sub.run(["sudo", "-u", "postgres", "psql", "-d", "tm_db", "-c","grant all on table users to " + user + ";"])
#sub.run(["sudo", "-u", "postgres", "psql", "-d", "tm_db", "-c","grant all on schema public to " + user + ";"])
#sub.run(["sudo","-k"])

def FETCH_SQL(sql_query):
    with psycopg.connect("dbname=tm_db") as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            try :
                cur.execute(sql_query)
                logger.info(time.asctime(time.gmtime())+f" : Executed SQL query: {sql_query}")
                response = cur.fetchall()
                logger.info(time.asctime(time.gmtime())+f" : Fetched data: {response}")
                return response
            except Exception as e:
                logger.error(time.asctime(time.gmtime())+" : "+str(e))
            
    
