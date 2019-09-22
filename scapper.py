import urllib3
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import asyncio

site = 'https://www.yahoo.com/news/weather'

async def scrapper(url):
    http = urllib3.PoolManager()
    while True:
        page = http.request('GET', url)
        soup = BeautifulSoup(page.data, "html.parser")
        # Extract location info
        Location = soup.find('div', attrs={'class': 'location'})
        Country = Location.contents[1]
        Town = Location.contents[0]

        # Extract Weather info
        Temp = soup.find('div', attrs={'class': 'temperature'})
        Condition = Temp.contents[0]
        Range = Temp.contents[1]
        Avrg = Temp.contents[2]

        # Clean info
        clean = lambda x: x.text.strip()
        row = [clean(x) for x in [Country, Town, Condition, Range, Avrg]]
        row.append(datetime.now())
        row.append(url)

        # Save to file
        with open('weather-data.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)

        print("Data point acquired at: {}".format(datetime.now()))
        await asyncio.sleep(30)

asyncio.run(scrapper(site))
