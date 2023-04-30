
import time

BASE_URL = 'https://realpython.com'
PATH_TO_LINKS = './posts/links.txt'
PATH_TO_POSTS = './posts/' + time.strftime("%Y-%m-%d") + '/'

# звідки брати пости для трансформації в markdown, яку дату сетати їм, куди зберігати
POSTS_TO_MD = PATH_TO_POSTS
MD_SET_DATE = time.strftime("%Y-%m-%d")
PATH_TO_MDPOSTS = './md_posts/' + MD_SET_DATE + '/'

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

MD_PROPS = ['layout: post']
