
import time

BASE_URL = 'https://realpython.com'
PATH_TO_LINKS = './posts/links.txt'
PATH_TO_POSTS = './posts/' + time.strftime("%Y-%m-%d") + '/'

TITLE_SELECTOR = 'h1'

DEL_TAGS = [["div", {"class": "container"}],
            "script",
            "footer",
            "iframe",
            "img",
            "bloquote",
            "figure",
            "a",
            "audio",
            "video",
            "svg",
            "form",
            "textarea",
            "input",
            "noscript",
            "progress"]
STRIP_TAGS = [["div", {"class": "article-body"}],
              "strong",
              "i",]
