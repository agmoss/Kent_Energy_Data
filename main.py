# Create scraper object on timed routine
# Return the db tables
# Insert data to MySQL db

import kent_scraper as ks
import db_functions as db


scr = ks.TableScraper()
tables = scr.db_tables('https://charting.kentgroupltd.com/WPPS_Public/DPPS_Public.htm')


regular = tables['regular']

#listed = regular.values.tolist()

conn = db.connect()

statement = db.sql_writer_insert("regular",'city','price','plus_minus','excl_taxes','margin','Date')

#db.insert_record(conn,regular[0],statement)


db.update_table(db.insert_record,conn,regular,statement)