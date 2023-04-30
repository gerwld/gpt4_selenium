import re


def clearSoup(content):
    content.attrs = {}
    for tags in content.findAll(True):
        if len(tags.get_text(strip=True)) == 0 and tags.name not in ['br', 'img']:
            tags.extract()
        tags.attrs = {}
    prettified = content.prettify()
    # [^\x00-\x7F]+ видаляє всі non-ASCII
    trimmedText = re.sub(r'[^\x00-\x7F]+', '', str(prettified))
    trimmedTextNoDoubleSpaces = re.sub(r'\n  ', ' ', str(trimmedText)).strip()
    trimmedTextNoSpacesAtTheBegining = re.sub(
        r'\>\s+', '>', str(trimmedTextNoDoubleSpaces)).strip()

    trimmedNoAmp = re.sub(
        r'\&amp; ', '', str(trimmedTextNoSpacesAtTheBegining)).strip()
    return trimmedNoAmp
