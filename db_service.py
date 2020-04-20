import os

import MySQLdb

cursor = None

def get_db_connection():
    global cursor

    if not cursor:
        db = MySQLdb.connect(os.environ.get("DB_HOST"), os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"), os.environ.get("DB_NAME"))
        cursor = db.cursor()

    return cursor


