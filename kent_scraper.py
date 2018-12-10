import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import html5lib

class TableScraper:

    def get_soup(self,url):

        r = requests.get(url)

        print(r.status_code)
        soup = BeautifulSoup(r.content, 'html5lib')

        return soup

    def get_data_body(self,soup):

        table = soup.find('table') #There is only one table on this webpage
        table_rows = table.find_all('tr')

        res = []
        for tr in table_rows[4:83]: #Skip the first 4 rows
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

    def beautify_data(self,df):

        # Rename columns
        df.columns = ['city',
        'price','plus_minus','excl_taxes','margin',
        'price','plus_minus','excl_taxes','margin', 
        'price','plus_minus','excl_taxes','margin', 
        'price','plus_minus','excl_taxes','margin', 
        'price','plus_minus','excl_taxes',
        'price','plus_minus','excl_taxes',
        ]

        df = df[1:] #take the data less the header row

        # This is faster 
        # df.drop(df.index[0])

        return df

    def get_date(self,soup):

        tr = soup.select('tbody > tr')[2]
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]

        return row[0]

    def db_tables(self,url):

        # table_names = ['Regular','Mid-Grade','Premium','Diesel','Automotive_Propane','Furnace_Oil']

        soup = self.get_soup(url)
        df = self.get_data_body(soup)

        # Dictionary of tables
        df_dict = {
            "regular": pd.DataFrame(df.iloc[:,0:5]),
            "mid_grade": pd.DataFrame(df.iloc[:,[0,6,7,8]]),
            "Premium": pd.DataFrame(df.iloc[:,[0,9,10,11,12]]),
            "Diesel": pd.DataFrame(df.iloc[:,[0,3]]),
            "Automotive_Propane": pd.DataFrame(df.iloc[:,[0,3]]),
            "Furnace_Oil": pd.DataFrame(df.iloc[:,[0,3]]),
        }

        #Add the date field
        for key,value in df_dict.items():
            value['Date'] = self.get_date(soup)

        # Convert to dictionary of lists
        table_list = {}
        for key, value in df_dict.items():

            value = value.values.tolist()
            table_list.update({key:value})

        return table_list


if __name__ == "__main__":

    scr = TableScraper()
    tables = scr.db_tables('https://charting.kentgroupltd.com/WPPS_Public/DPPS_Public.htm')
    
    df = tables['regular']

    print(df)
 