import logging
import mysql.connector


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

    try:
        host, user, password, db = config()

        conn = mysql.connector.connect(host=host,
                                       database=db,
                                       user=user,
                                       password=password)

    # make these raise to return?
    except mysql.connector.errors.ProgrammingError as e:
        logging.info(e)
        raise

    except mysql.connector.errors.InterfaceError as e:
        logging.info(e)
        raise

    except Exception as ex:
        logging.info(ex)
        raise

    return conn


def insert_many(db, val, sql):
    """Insert the list of records"""

    try:
        my_cursor = db.cursor()
        my_cursor.executemany(sql, val)
        db.commit()

    except Exception as ex:  # TODO Expand on exception handling (there should be some mysql error objects to access)
        logging.info(ex)
        raise


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


if __name__ == '__main__':
    connect(db_config)
