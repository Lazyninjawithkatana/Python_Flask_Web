import psycopg2
import os

HOST = os.environ.get('HOST', 'localhost')
USER = os.environ.get('USER', 'youruser')
PASSWORD = os.environ.get('PASSWORD', 'yourpassword')
DATABASE = os.environ.get('DATABASE', 'postgres')
NEW_DB_NAME = 'yourprojectname'