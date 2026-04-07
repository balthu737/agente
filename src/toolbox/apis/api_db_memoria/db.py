import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def conexcion():
    return mysql.connector.connect(
        host = os.getenv("MYSQL_HOST"),
        port = int(os.getenv("MYSQL_PORT")),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        database = os.getenv("MYSQL_DB")
    )
