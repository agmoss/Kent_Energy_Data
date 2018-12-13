import logging
import time

import schedule

import db_functions as db
import kent_scraper as ks


def main():
    """main method"""

    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Start')

    scr = ks.TableScraper('https://charting.kentgroupltd.com/WPPS_Public/DPPS_Public.htm')

    if scr.status_code() != 200:
        logging.info('Kent data website unavalible. Status code: ' + scr.status_code())
        # Run main method after a delay
    else:

        try:

            # Create the tables
            tables = scr.db_tables()
            logging.info('Tables created')

            # Connect to the database
            conn = db.connect(db.db_config)

            # Insert to the regular table
            statement = db.sql_writer_insert('regular', 'city', 'price', 'plus_minus', 'excl_taxes', 'margin',
                                                'Date')

            status = db.insert_many(conn, tables['regular'], statement)

            if status:
                logging.info('Regular data inserted')
            else:
                raise Exception

            conn.close()

        except Exception as ex:
            
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            
        finally:
            
            #TODO Is the finally necessary, what should I put here???
            pass

            
if __name__ == "__main__":

    schedule.every(0.001).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
