import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from helpers.filterValidLinks import filterValidLinks
from global_context import PATH_TO_LINKS, PATH_TO_POSTS, DEL_TAGS, STRIP_TAGS, TITLE_SELECTOR, FETCH_NO_TAGS, DEL_CLASS, DEL_PHRASES
from helpers.createPost import *
from helpers.clearSoup import *
from helpers.stripSoup import *
from helpers.delTagsSoup import *
from helpers.delPhrasesSoup import *


# Ініціалізація сервісу, опшинів хедлес бравзеру
chromedriver = '/usr/local/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
service = ChromeService(executable_path=chromedriver)
browser = webdriver.Chrome(service=service, options=options)

# отримання ссилок і мепінг в массив
with open(PATH_TO_LINKS, 'r') as f:
    links = f.read().split("\n")
    uniqueLinks = list(filterValidLinks(links))

    if (len(uniqueLinks)):
        print(f'Successfully parsed links from ' +
              PATH_TO_LINKS + '... Please wait...')
    elif not len(f):
        print('Theres no links')
    else:
        print('Some error occured')

# скрапінг постів і запис їх в .md
if uniqueLinks and len(uniqueLinks):
    for link in uniqueLinks:
        browser.get(link)
        postHtml = browser.page_source
        postSoup = BeautifulSoup(
            postHtml, 'html5lib').find(id="main")
        print(f'Getting post from {link}')
        postTitle = postSoup.find(
            TITLE_SELECTOR).get_text()

        # трімінг супа
        for tag in DEL_TAGS:
            for match in postSoup.find_all(tag):
                match.decompose()

        for tag in DEL_CLASS:
            for match in postSoup.find_all(class_=tag):
                match.decompose()

        # трімінг супа в залежності чи залишити теги
        clearedSoup = clearSoup(postSoup)
        noTagedSoup = delTagsSoup(postSoup)
        finalPost = (clearedSoup, noTagedSoup)[FETCH_NO_TAGS]

        strFinalPost = stripSoup(finalPost, STRIP_TAGS)
        delPhFinalPost = delPhrasesSoup(strFinalPost, DEL_PHRASES)

        delay = random.randint(1, 4)
        createPost(postTitle, delPhFinalPost, delay)
        time.sleep(delay)

    print(PATH_TO_POSTS)

    browser.quit()
