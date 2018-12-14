import pytest

from ..scripts import db_functions as db

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