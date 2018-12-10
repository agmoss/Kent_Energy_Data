# Config
import json

with open('config.json', 'r') as f:
    config = json.load(f)

host = config['DATABASE_CONFIG']['host'] 
user = config['DATABASE_CONFIG']['user'] 
password = config['DATABASE_CONFIG']['password'] 
db = config['DATABASE_CONFIG']['dbname'] 


import mysql.connector
from mysql.connector import Error
 
def connect():
    """ Connect to MySQL database """

    try:
        conn = mysql.connector.connect(host=host,
                                       database=db,
                                       user=user,
                                       password=password)
        if conn.is_connected():
            print('Connected to MySQL database')
 
    except Error as e:
        print(e)
 
    # finally:
    #     conn.close()

    return conn

def insert_record(mydb,record,sql):

    mycursor = mydb.cursor()

    mycursor.execute(sql, record)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

def update_table(func,db_conn,records,sql):

    for x in records:
        func(db_conn,x,sql)

def sql_writer_insert(table_name, *args):

    header_list = []
    s_list = []
    for value in args:
        header_list.append(value)
        s_list.append('%s')

    #Convert
    header_list = ','.join(map(str, header_list)) 
    s_list = ','.join(map(str, s_list)) 

    sql = "INSERT INTO " + table_name + " (" + header_list + ") " +  "VALUES"  + " (" + s_list + ")"

    return sql


if __name__ == '__main__':
    
    connect()