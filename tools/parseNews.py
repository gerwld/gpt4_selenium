import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from helpers.filterValidLinks import filterValidLinks
from global_context import PATH_TO_LINKS, PATH_TO_POSTS, DEL_TAGS, STRIP_TAGS, TITLE_SELECTOR, FETCH_NO_TAGS
from helpers.createPost import createPost
from helpers.clearSoup import clearSoup
from helpers.stripSoup import stripSoup
from helpers.delTagsSoup import delTagsSoup


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
            postHtml, 'html5lib').select_one('.article-body')
        print(f'Getting post from {link}')
        postTitle = postSoup.find(
            TITLE_SELECTOR).get_text()

        # трімінг супа
        for tag in DEL_TAGS:
            delTagAll = postSoup.find_all(tag)
            for match in delTagAll:
                match.decompose()
        stripedSoup = stripSoup(postSoup, STRIP_TAGS)

        # трімінг супа в залежності чи залишити теги
        clearedSoup = clearSoup(stripedSoup)
        noTagedSoup = delTagsSoup(stripedSoup)
        finalPost = (clearedSoup, noTagedSoup)[FETCH_NO_TAGS]

        delay = random.randint(2, 8)
        createPost(postTitle, finalPost, delay)
        time.sleep(delay)

    print(PATH_TO_POSTS)

    browser.quit()
