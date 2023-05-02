from bs4 import BeautifulSoup
import re


def stripSoup(soup, strip_tags):
    # преобразує в суп
    locSoup = soup
    if type(soup) == str:
        locSoup = BeautifulSoup(soup, 'html5lib')

    # удаляє strip_tags теги заміняючи на <></>
    for tag in locSoup.findAll(True):
        if tag.name in strip_tags:
            tag.name = ''
    # удаляє <></>
    locSoup = re.sub(r'<>|</>|  ', '', str(locSoup))

    # повертає суп
    newSoup = BeautifulSoup(locSoup, 'html5lib')

    return newSoup.find('body')
