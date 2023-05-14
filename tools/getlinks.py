import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from global_context import PATH_TO_LINKS, BASE_URL

# Ініціалізація сервісу, опшинів хедлес бравзеру
chromedriver = '/usr/local/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
service = ChromeService(executable_path=chromedriver)
browser = webdriver.Chrome(service=service, options=options)

# Переход на сторінку i отримання змісту
browser.get(BASE_URL)
requiredHtml = browser.page_source

# Парсінг всіх ссилок на пости
soup = BeautifulSoup(requiredHtml, 'html5lib')
parentDiv = soup.find(id="main-box-1")
allLinksToArticles = parentDiv.select('.entry-title:has(a)')

allLinksToArticlesInline = ''
for h2 in allLinksToArticles:
    link = h2.find('a')
    allLinksToArticlesInline += (link['href'] + '\n')

# створення нового файлу з усіма лінками
if allLinksToArticlesInline:
    count = allLinksToArticlesInline.count('\n')

    os.makedirs(os.path.dirname(PATH_TO_LINKS), exist_ok=True)
    with open(PATH_TO_LINKS, 'w+') as f:
        f.write(allLinksToArticlesInline)
    print(f'Successfully added {count} links to ' + PATH_TO_LINKS)


browser.quit()
