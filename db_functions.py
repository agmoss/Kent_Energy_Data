# Config
def db_config():

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

    #Default return value
    conn = None

    try:
        host,user,password,db = db_config()

        conn = mysql.connector.connect(host=host,
                                        database=db,
                                        user=user,
                                        password=password)

    except mysql.connector.errors.ProgrammingError as e:
        print("Configuration error")

    except mysql.connector.errors.InterfaceError as e:
        print("The database is offline")

    return conn

def insert_record(mydb, record, sql):

    #Default return value
    insert = False

    try:
        my_cursor = mydb.cursor()
        my_cursor.execute(sql, record)
        mydb.commit()
        insert = True
        # print(my_cursor.rowcount, "record inserted.")

    except Exception as e: #Expand on exception handling
        print (e)
        

    return insert

def update_table(func, db_conn, records, sql):
    for x in records:
        func(db_conn, x, sql)

def sql_writer_insert(table_name, *args):
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
    connect()
