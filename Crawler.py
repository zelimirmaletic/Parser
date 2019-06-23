from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get('http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=urb_cpop1&lang=en')


#response = requests.get('http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=urb_cpop1&lang=en')

lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False
while(match==False):
                lastCount = lenOfPage
                time.sleep(3)
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match = True

response = driver.execute_script("return document.documentElement.outerHTML")

soup = BeautifulSoup(''.join(response), 'html.parser')

box = soup.find('div', {'class':'ptYCol'})
allCityBoxes = box.findAll('div', {'class':'ptYDim'})
print(len(allCityBoxes))

citiesList = []

for box in allCityBoxes:
	citiesList.append(box.find('div').text)

for city in citiesList:
	print(city)
	

#driver.quit()

