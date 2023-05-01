
import time

BASE_URL = 'https://realpython.com'

PATH_TO_LINKS = './res/posts/links.txt'
PATH_TO_POSTS = './res/posts'
PATH_TO_MDPOSTS = './res/md_posts'

# префікс для генератора MD. Працює в обі сторони
MD_PREFIX = ''

# звідки брати пости для трансформації в markdown, яку дату сетати їм, куди зберігати
MD_SET_DATE = time.strftime("%Y-%m-%d")
POSTS_TO_MD = PATH_TO_POSTS + MD_PREFIX + "/" + MD_SET_DATE + "/"

# чи фетчити без тегів
FETCH_NO_TAGS = True

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
            "progress",
            "style"]
STRIP_TAGS = [["div", {"class": "article-body"}],
              "strong",
              "i",]

MD_PROPS = ['layout: post']
