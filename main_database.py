import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import database_const

#Local postgres db connection and new db creation
#Connect to local postgres db
def connect_postgres_creation_db():
    cur = None
    conn = None
    #Db postgres connection
    try:
        conn = psycopg2.connect(
            host=database_const.HOST,
            user=database_const.USER,
            password=database_const.PASSWORD,
            database=database_const.DATABASE
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        try:
            cur.execute(f'CREATE DATABASE {database_const.NEW_DB_NAME}')
            print(f'[+] Database {database_const.NEW_DB_NAME} created sucessfully!')
        except psycopg2.errors.DuplicateDatabase as e:
            print(f'[!] Error with {e}')
    except psycopg2.Error as e:
        print(f'[!] Error with {e}')
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    #Create tables
    #Connect to new DB
    conn = psycopg2.connect(
        host=database_const.HOST,
        user=database_const.USER,
        password=database_const.PASSWORD,
        database=database_const.NEW_DB_NAME
    )
    cur = conn.cursor()
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """
    try:
        cur.execute(create_users_table)
        conn.commit()
        print('[+] Successfully created table')
    except psycopg2.Error as e:
        print(f'[!] Error with {e}')
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    connect_postgres_creation_db()
