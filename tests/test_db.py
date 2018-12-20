import pytest

from ..scripts import db_functions as db
from ..scripts import kent_scraper as ks

# Test the database functions
#import db_functions as db

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
    
    with pytest.raises(Exception) as e_info:

        connection = db.connect(sample)


def test_insert_many_bad_data():

    # Scraper object
    scr = ks.TableScraper('https://charting.kentgroupltd.com/WPPS_Public/DPPS_Public.htm')

    # Create the scraped tables
    tables = scr.db_tables()

    # Corrupt the data

    for x in tables['regular']:
        del x[2]

    # Connect to the database (exception raised if not connected)
    conn = db.connect(db.db_config)

    # Create SQL statement
    statement = db.sql_writer_insert('regular', 'city', 'price', 'plus_minus', 'excl_taxes', 'margin',
                                        'Date')


    conn.close()
    
    with pytest.raises(Exception) as e_info:

        # Insert to the regular table
        db.insert_many(conn, tables['regular'], statement)  # exception raised if data not inserted


    
