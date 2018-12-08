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
 
def connect(dbname):
    """ Connect to MySQL database """

    if dbname != config['DATABASE_CONFIG']['dbname']:
        raise ValueError("Couldn't not find DB with given name")

    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='python_mysql',
                                       user='root',
                                       password='secret')
        if conn.is_connected():
            print('Connected to MySQL database')
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
 

if __name__ == '__main__':
    connect(name)