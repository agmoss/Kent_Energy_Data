# Daily Pump Price ETL

This program scrapes daily pricing data of petrolium products in major canadian cities. The retrieved data is cleaned and stored in a MySQL database for safe storage and analysis.

Scraper target:

https://charting.kentgroupltd.com/WPPS_Public/DPPS_Public.htm

## Instructions

The use of this program requires a live MySQL database. Please view the database documentation for the required schema.

Database credentials must be placed in the config.json file. A blank config file is provided for your convienence. 

### Prerequisites

Dependencies can be installed via...

```
pip install requirements.txt
```

### Installing


The entry point of the program is the main.py file. After cloning the repository, it can be accessed via...

```
cd Kent_Energy_Data
```

```
python3 main.py
```

view the app.log file for runtime information


To access the data use a MySQL client. 

```
http://123.123.0.12/phpmyadmin/
```

## Running the tests

Testing for this project is handled by pytest.

### Testing the database connection

The test_db.py file contains thorough testing of the database connection. In the project directory, type:

```
$ pytest
```

All tests should pass before proceeding.

## Deployment

This system can be deployed on a remote MySQL instance. Ensure the port 3306 is open on your system and that your MySQL server is bound to the servers IP address.

## Built With

* [Requests](http://docs.python-requests.org/en/master/) - Browser
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Parser
* [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) - MySQL driver written in python

## Contributing

Feedback and constructive criticism is more than welcome


## Authors

* **Andrew Moss** - *Creator* - [agmoss](https://github.com/agmoss)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details




