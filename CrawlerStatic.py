from bs4 import BeautifulSoup
import requests
import sys

class Crawler:
    citiesList = []
    regex = ''

    def scrapeWebLink(self):
        response = requests.get('https://www.worldatlas.com/citypops.htm')
        bs = BeautifulSoup(response.text, "lxml")
        table_body=bs.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols=row.find_all('td')
            cols=[x.text.strip() for x in cols]
            self.citiesList.append(cols[1])
        # We will sort list for better performance in later search
        self.citiesList.sort()

    def printList(self):
        for item in self.citiesList:
            print(item)

    def formRegex(self):
        for index,city in enumerate(self.citiesList):
            self.regex += city
            if index != len(self.citiesList)-1:
                self.regex+='|'

# ----------TESTING CODE---------
#myCrawler = Crawler()
#myCrawler.scrapeWebLink()
#myCrawler.printList()
#myCrawler.formRegex()
#print('Extracted regex:')
#print(myCrawler.regex)
