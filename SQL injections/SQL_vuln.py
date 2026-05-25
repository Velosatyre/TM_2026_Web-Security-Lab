import psycopg

with psycopg.connect("dbname=test_db user=artur") as conn:
    with conn.cursor() as cur:
        cur.execute("select * from cars")
        print(cur.fetchall())