import psycopg2
import os

def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])