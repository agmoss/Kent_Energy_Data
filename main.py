import logging
import time

import schedule

import db_functions as db
import kent_scraper as ks


def main():
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
            conn = db.connect()

            if conn.is_connected():
                # Insert to the regular table
                statement = db.sql_writer_insert('regular', 'city', 'price', 'plus_minus', 'excl_taxes', 'margin',
                                                 'Date')
                db.update_table(db.insert_record, conn, tables['regular'], statement)
                logging.info('Regular data inserted')

                # Insert to the mid grade table
                statement = db.sql_writer_insert('mid_grade', 'city', 'price', 'plus_minus', 'excl_taxes', 'margin',
                                                 'Date')
                db.update_table(db.insert_record, conn, tables['mid_grade'], statement)
                logging.info('Mid grade data inserted')

        except Exception as ex:

            logging.info("An exception occurred: " + ex.args)

        finally:

            conn.close()


if __name__ == "__main__":

    schedule.every(0.001).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
