import os

import psycopg2

cursor = None

def get_db_connection():
    global cursor

    if not cursor:
        db = psycopg2.connect( host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"), dbname=os.environ.get("DB_NAME") )
        cursor = db.cursor()

    return cursor


