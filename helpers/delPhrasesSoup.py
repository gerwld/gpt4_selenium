import re


def delPhrasesSoup(soup, phrases):
    res = soup
    for phrase in phrases:
        res = re.sub(phrase, ' ', str(soup)).strip()
    return res
