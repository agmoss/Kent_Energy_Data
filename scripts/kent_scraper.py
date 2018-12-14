import pandas as pd
import requests
from bs4 import BeautifulSoup


class TableScraper:

    def __init__(self, url):
        self.url = url

    def get_soup(self):

        r = requests.get(self.url)

        if r.status_code != 200:
            raise Exception("Kent website offline!")  # Handled by the caller
        else:
            soup = BeautifulSoup(r.content, 'html5lib')

        return soup

    def get_data_body(self, soup):

        table = soup.find('table')  # There is only one table on this webpage
        table_rows = table.find_all('tr')

        res = []
        for tr in table_rows[4:83]:  # Skip the first 4 rows
            td = tr.find_all('td')
            row = [tr.text.strip() for tr in td if tr.text.strip()]
            if row:
                res.append(row)

        df = pd.DataFrame(res)

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return self.beautify_data(df)

    def beautify_data(self, df):

        # Rename columns
        df.columns = ['city',
                      'price', 'plus_minus', 'excl_taxes', 'margin',
                      'price', 'plus_minus', 'excl_taxes', 'margin',
                      'price', 'plus_minus', 'excl_taxes', 'margin',
                      'price', 'plus_minus', 'excl_taxes', 'margin',
                      'price', 'plus_minus', 'excl_taxes',
                      'price', 'plus_minus', 'excl_taxes',
                      ]

        df = df[1:]  # take the data less the header row

        return df

    def get_date(self, soup):

        tr = soup.select('tbody > tr')[2]
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]

        return row[0]

    def db_tables(self):

        try:

            soup = self.get_soup()
            df = self.get_data_body(soup)

            # Dictionary of tables
            df_dict = {
                "regular": pd.DataFrame(df.iloc[:, 0:5]),
                "mid_grade": pd.DataFrame(df.iloc[:, [0, 5, 6, 7, 8]]),
                "premium": pd.DataFrame(df.iloc[:, [0, 9, 10, 11, 12]]),
                "diesel": pd.DataFrame(df.iloc[:, [0, 13, 14, 15, 16]]),
                "automotive_propane": pd.DataFrame(df.iloc[:, [17, 18, 19]]),
                "furnace_oil": pd.DataFrame(df.iloc[:, [20, 21, 22]]),
            }

            # Add the date field
            for key, value in df_dict.items():
                value['Date'] = self.get_date(soup)

            # Convert to dictionary of lists
            table_list = {}
            for key, value in df_dict.items():
                value = value.values.tolist()
                table_list.update({key: value})

            return table_list

        except Exception("Cannot create the scraped tables"):
            raise  # handled by the caller


if __name__ == "__main__":
    print(__name__)