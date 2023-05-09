"""Чистить суп від non-ASCII, вайтспейсів ітд"""
import re


def clearSoup(content):
    content.attrs = {}
    for tags in content.findAll(True):
        if len(tags.get_text(strip=True)) == 0 and tags.name not in ['br', 'img']:
            tags.extract()
        tags.attrs = {}
    prettified = content.prettify()
    # [^\x00-\x7F]+ видаляє всі non-ASCII
    t = re.sub(r'[^\x00-\x7F]+', '', str(prettified))
    tNoDoubleSpaces = re.sub(r'\n  ', ' ', str(t)).strip()
    tNoSpacesAtTheBegining = re.sub(
        r'\>\s+', '>', str(tNoDoubleSpaces)).strip()

    trimmedNoAmp = re.sub(
        r'\&amp; ', '', str(tNoSpacesAtTheBegining)).strip()
    trimmedNoBrokenTag = re.sub(
        r'<<', '<', str(trimmedNoAmp)).strip()
    trimmedNoBrokenTag2 = re.sub(
        r'</<', '<', str(trimmedNoBrokenTag)).strip()

    return trimmedNoBrokenTag2
