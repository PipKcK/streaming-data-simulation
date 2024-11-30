import psycopg2
import os

def get_connection():
    db_url = os.environ["DATABASE_URL"]
    ssl_cert_path = os.environ["SSL_CERT_PATH"]
    return psycopg2.connect(f"{db_url}&sslrootcert={ssl_cert_path}")