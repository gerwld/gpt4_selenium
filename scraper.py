from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService

# Ініціалізація сервісу, опшинів хедлес бравзеру
chromedriver = '/usr/local/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
service = ChromeService(executable_path = chromedriver);
browser = webdriver.Chrome(service=service, options=options)

# Переход на сторінку i отримання змісту
BASE_URL = 'https://realpython.com'
browser.get(BASE_URL + '/search')
requiredHtml = browser.page_source

# Парсінг всіх ссилок на пости
soup = BeautifulSoup(requiredHtml, 'html5lib')

parentDiv = soup.find(id = "resultsArea");
allLinksToArticles = parentDiv.select('.stretched-link')

for a in allLinksToArticles:
    print("Found the URL:", BASE_URL + a['href'])