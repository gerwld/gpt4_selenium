from bs4 import BeautifulSoup
from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):

    soup = BeautifulSoup(body, 'html5lib')
    print(body)
    # texts = soup.findAll(text=True)
    # visible_texts = filter(tag_visible, texts)
    # return u" ".join(t.strip() for t in visible_texts)
