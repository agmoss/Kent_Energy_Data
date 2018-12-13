import logging

# Config
def db_config():
    """Setup"""

    import json

    with open('config.json', 'r') as f:
        config = json.load(f)

    host = config['DATABASE_CONFIG']['host']
    user = config['DATABASE_CONFIG']['user']
    password = config['DATABASE_CONFIG']['password']
    db = config['DATABASE_CONFIG']['dbname']

    return host,user,password,db


import mysql.connector
from mysql.connector import Error


def connect(db_config):
    """ Connect to MySQL database """

    try:
        host,user,password,db = db_config()

        conn = mysql.connector.connect(host=host,
                                        database=db,
                                        user=user,
                                        password=password)
        
    #make these raise to return?
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

def insert_many(mydb,val,sql):
    """Insert the list of records"""
    
    try:
        my_cursor = mydb.cursor()
        my_cursor.executemany(sql, val)
        mydb.commit()

    except Exception as ex: #Expand on exception handling
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

########

def insert_record(mydb, record, sql):
    """depricated"""
    #Default return value
    insert = False

    try:
        my_cursor = mydb.cursor()
        my_cursor.execute(sql, record)
        mydb.commit()
        insert = True
        # print(my_cursor.rowcount, "record inserted.")

    except Exception as ex: #Expand on exception handling
        
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        
    return insert

def update_table(func, db_conn, records, sql):
    """depricated"""

    for x in records:
        func(db_conn, x, sql)


if __name__ == '__main__':
    connect(db_config)
