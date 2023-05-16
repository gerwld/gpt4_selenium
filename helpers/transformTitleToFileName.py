from helpers.onlyAllowed import *


def transformTitleToFileName(title, format=""):
    trimedTitleArr = map(str.lower, onlyAllowed(
        my_string=title).split(' '))
    return "-".join(filter(lambda x: len(x), trimedTitleArr)) + format
