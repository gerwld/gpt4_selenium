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

    # Стріпає текст всередині тегів окрім code і pre
    for tag in locSoup.findAll(True):
        if tag.name not in ['code', 'pre']:
            if tag.string:
                tag.string = str(tag.string).strip()

    # видаляє тег p якщо починається з кортежу або містить більше ніж один знак наголосу
    for tag in locSoup.find_all('p'):
        if tag.get_text() and tag.get_text().strip().lower().startswith(('read also', 'thank you')):
            tag.decompose()
        if tag.get_text() and ('!!') in tag.get_text().strip().lower():
            tag.decompose()

    # удаляє <></>
    locSoup = re.sub(r'<>|</>|  ', '', str(locSoup))
    locSoup = re.sub(r'<<|', '<', str(locSoup))
    locSoup = re.sub(r'>>', '>', str(locSoup))
    locSoup = re.sub(r'>/>', '/>', str(locSoup))
    locSoup = re.sub(r'</<', '</', str(locSoup))
    locSoup = re.sub(r'</</', '</', str(locSoup))
    locSoup = re.sub(r'</</<', '</', str(locSoup))

    # повертає суп
    newSoup = BeautifulSoup(locSoup, 'html5lib')
    newSoup.find('body').name = 'article'

    return newSoup.find('article')
