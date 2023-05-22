import re


def delPhrasesSoup(soup, phrases):
    res = str(soup)
    for phrase in phrases:
        ed_res = re.sub(phrase, " ", res)
        res = ed_res
    return res
