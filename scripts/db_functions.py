import logging
import mysql.connector
import time
import sys


def db_config():
    """Setup"""

    import json

    with open('config.json', 'r') as f:
        config = json.load(f)

    host = config['DATABASE_CONFIG']['host']
    user = config['DATABASE_CONFIG']['user']
    password = config['DATABASE_CONFIG']['password']
    db = config['DATABASE_CONFIG']['dbname']

    return host, user, password, db


def connect(config):
    """ Connect to MySQL database """

    while True:

        try:
            host, user, password, db = config()

            conn = mysql.connector.connect(host=host,
                                        database=db,
                                        user=user,
                                        password=password)

        except mysql.connector.errors.ProgrammingError as e:

            if e.errno == 1049:  # Database not created yet
                create_db()
                #connect(db_config)
            elif e.errno == 1045:
                logging.info("FATAL:Access denied: password or db name incorrect")
                logging.info(e)
                sys.exit(-1)
            else:
                logging.info(e)
                raise

        except mysql.connector.errors.InterfaceError as e:

            if e.errno == 2003:
                logging.info("FATAL:Connection to the database has been refused")
                logging.info(e)
                sys.exit(-1)

        except Exception as ex:
            logging.info(ex)
            raise

        else:
            return conn


def insert_many(db, val, sql):
    """Insert the list of records"""

    while True:

        try:
            my_cursor = db.cursor()
            my_cursor.executemany(sql, val)
            db.commit()

        except mysql.connector.errors.ProgrammingError as e:

            if e.errno == 1146:  # Database table not created yet
                create_tables(db)

        except Exception as ex:  # TODO Expand on exception handling (there should be some mysql error objects to access)
            logging.info(ex)
            print(type(ex))
            raise

        else:
            break


def sql_writer_insert(table_name, *args):
    """Generate a custom SQL insert statement"""
    header_list = []
    s_list = []
    for value in args:
        header_list.append(value)
        s_list.append('%s')

    # Convert
    header_list = ','.join(map(str, header_list))
    s_list = ','.join(map(str, s_list))

    sql = "INSERT INTO " + table_name + " (" + header_list + ") " + "VALUES" + " (" + s_list + ")"

    return sql

def create_db():
    try:
        host, user, password, db = db_config()

        conn = mysql.connector.connect(host=host,
                                       user=user,
                                       password=password)

        mycursor = conn.cursor()

        mycursor.execute("CREATE DATABASE " + db)

        logging.info('Database created')

    except Exception as ex:  # TODO: Handle this
        logging.info(ex)
        raise

def create_tables(conn):

    tables = ["regular", "mid_grade","premium", "diesel", "automotive_propane", "furnace_oil"]

    try:
        # Determine if table already exists
        mycursor = conn.cursor()
        mycursor.execute("SHOW TABLES")

        for table in tables:

            if table not in mycursor:

                mycursor.execute("CREATE TABLE " + table + 
                "(city VARCHAR(255), price VARCHAR(255), plus_minus VARCHAR(255), excl_taxes VARCHAR(255), margin VARCHAR(255), date VARCHAR(255))")  # TODO: construct a proper statement

    except Exception as ex:
        logging.info(ex)
        raise


if __name__ == '__main__':
    connect(db_config)
