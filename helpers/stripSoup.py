from bs4 import NavigableString


def stripSoup(soup, strip_tags):
    for tag in soup.findAll(True):
        if tag.name in strip_tags:
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = stripSoup(str(c), strip_tags)
                s += str(c)
            tag.replaceWith(s)
    return soup
