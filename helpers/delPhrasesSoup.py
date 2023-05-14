import re


def delPhrasesSoup(soup, phrases):
    res = soup
    for phrase in phrases:
        res = str(res).replace(phrase, ' ').strip()
    return res
