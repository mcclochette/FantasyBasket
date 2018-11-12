#!/usr/bin/python
import psycopg2
from ConfigParser import ConfigParser
import os


def config(filename=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.ini'), section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = ""
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db += param[0]
            db += "="
            db += param[1]
            db += " "

    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute("Select * from team")

        # display the PostgreSQL database server version
        rows = cur.fetchall()
        for row in rows:
            for ro in row:
                print (ro, " ")

        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
