import logging
import time

import schedule

from scripts import db_functions as db
from scripts import kent_scraper as ks


def main():
    """main method"""

    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Start')

    #Scraper object
    scr = ks.TableScraper('https://charting.kentgroupltd.com/WPPS_Public/DPPS_Public.htm')

    try:

        # Create the tables
        tables = scr.db_tables()
        logging.info('Tables created')

        # Connect to the database (exception raised if not connected)
        conn = db.connect(db.db_config)
        logging.info('Connected to the database')

        # Create SQL statement
        statement = db.sql_writer_insert('regular', 'city', 'price', 'plus_minus', 'excl_taxes', 'margin',
                                            'Date')

        # Insert to the regular table
        db.insert_many(conn, tables['regular'], statement) # exception raised if data not inserted

        logging.info('Regular data inserted') #Successfull insert

        conn.close()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.info(message)
        
    finally:
        logging.info("Run Complete")

            
if __name__ == "__main__":

    schedule.every(0.001).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
