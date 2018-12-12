import pytest

# Test the database functions
import db_functions as db

# Test connect()
def test_connection_success():
    connection = db.connect(db.db_config)
    assert connection != None 


def test_connection_failure():
    #Test function
    def sample():
        a = "fakehost"
        b = "fakeuser"
        c = "fake password"
        d = "fake db"

        return a,b,c,d

    connection = db.connect(sample)
    assert connection == None

def test_insert_record_success():

    #Instantate the necessary paramaters
    connection = db.connect(db.db_config)
    record = ['Test',1,1,1,1,'Test']
    statement = db.sql_writer_insert('regular', 'city', 'price', 'plus_minus', 'excl_taxes', 'margin', 'Date')

    status = db.insert_record(connection,record,statement)

    assert status == True


def test_insert_record_failure():

    # Instantate the necessary paramaters
    connection = db.connect(db.db_config)
    record = ['Test',1,1,1,1]
    statement = db.sql_writer_insert('regular', 'city', 'price', 'plus_minus', 'excl_taxes', 'margin', 'Date')

    status = db.insert_record(connection,record,statement)

    assert status == False
