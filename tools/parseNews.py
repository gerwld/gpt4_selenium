import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from helpers.filterValidLinks import filterValidLinks
from global_context import PATH_TO_LINKS, PATH_TO_POSTS, DEL_TAGS, STRIP_TAGS, TITLE_SELECTOR, FETCH_NO_TAGS, DEL_CLASS, DEL_PHRASES, C_RED
from helpers.createPost import *
from helpers.clearSoup import *
from helpers.stripSoup import *
from helpers.delTagsSoup import *
from helpers.delPhrasesSoup import *
from helpers.textFromHtml import *

MIN_WORDS_LENGTH = 250


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
            postHtml, 'html5lib')
        postContent = postSoup.find("article", class_="article-content")
        if postContent:
            postWordsLenth = len(
                " ".join(postContent.findAll(string=True)).strip().split(' '))

            # перевірка на довжину по кількості слів, якщо менше MIN_WORDS_LENGTH - скіп
            if postWordsLenth > MIN_WORDS_LENGTH:
                if postSoup.find(TITLE_SELECTOR) and len(postSoup.find(TITLE_SELECTOR)):
                    postTitle = postSoup.find(
                        TITLE_SELECTOR).get_text().strip()
                    print(f'Getting post from {link}\n')
                    print(f'Title: {postTitle}')

                    # якщо в контенті немає тайтлу але є в супі - додай в суп
                    if not postContent.find(TITLE_SELECTOR):
                        titleTag = postSoup.new_tag('h1')
                        titleTag.string = postTitle
                        postContent.p.insert_before(titleTag)
                        print("Inserted title inside article.")

                        # трімінг супа
                    for tag in DEL_TAGS:
                        for match in postContent.find_all(tag):
                            match.decompose()

                    for tag in DEL_CLASS:
                        for match in postContent.find_all(class_=tag):
                            match.decompose()

                    # трімінг супа в залежності чи залишити теги
                    clearedSoup = clearSoup(postContent)
                    noTagedSoup = delTagsSoup(postContent)
                    finalPost = (clearedSoup, noTagedSoup)[FETCH_NO_TAGS]

                    strFinalPost = stripSoup(finalPost, STRIP_TAGS)
                    delPhFinalPost = delPhrasesSoup(strFinalPost, DEL_PHRASES)
                    delPhFinalPostWithSource = '<del><a href="' + \
                        link + '"/>' + link + '</a></del>\n' + \
                        delPhFinalPost

                    delay = random.randint(0, 3)
                    createPost(
                        postTitle, delPhFinalPostWithSource, delay)
                    time.sleep(delay)
                else:
                    print(
                        f'{C_RED}Broken title in post from {link}. Skipping...{C_RED.OFF}')

            else:
                print(
                    f'{C_RED}Length is less than {MIN_WORDS_LENGTH} (has only: {postWordsLenth}) from {link}. Skipping...{C_RED.OFF}')

    print(PATH_TO_POSTS)

    browser.quit()
