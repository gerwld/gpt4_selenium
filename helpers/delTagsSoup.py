import re


def delTagsSoup(content):
    prettified = content.prettify()

    # [^\x00-\x7F]+ видаляє всі non-ASCII
    t = re.sub(r'[^\x00-\x7F]+', '', str(prettified))
    tNoDoubleSpaces = re.sub(r'\n  ', ' ', str(t)).strip()
    tNoSpacesAtTheBegining = re.sub(
        r'\>\s+', '>', str(tNoDoubleSpaces)).strip()

    trimmedNoAmp = re.sub(
        r'\&amp; ', '', str(tNoSpacesAtTheBegining)).strip()
    return trimmedNoAmp
