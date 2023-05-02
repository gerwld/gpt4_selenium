
import time
from colorist import ColorRGB

BASE_URL = 'https://linuxhint.com/'

PATH_TO_LINKS = './res/posts/links.txt'
PATH_TO_POSTS = './res/posts'
PATH_TO_MDPOSTS = './res/md_posts'

# префікс для генератора MD. Працює в обі сторони
MD_PREFIX = ''

# звідки брати пости для трансформації в markdown, яку дату сетати їм, куди зберігати
MD_SET_DATE = time.strftime("%Y-%m-%d")
POSTS_TO_MD = PATH_TO_POSTS + MD_PREFIX + "/" + MD_SET_DATE + "/"

# чи фетчити без тегів
FETCH_NO_TAGS = False

# ліміт по словам для фільтрації
MIN_WORDS_LIMIT = 700
MAX_WORDS_LIMIT = 5000


TITLE_SELECTOR = 'h1'

DEL_PHRASES = [
    "<p>Press&lt;Enter&gt;. </p>",
    "&lt;"
]

DEL_CLASS = [
    "entry-meta",
]

DEL_TAGS = [
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
    "button",
    "progress",
    "style"]
STRIP_TAGS = [
    "html",
    "head",
    "body",
    "main",
    "div",
    "strong",
    "span",
    "i",]

MD_PROPS = ['layout: post']

C_RED = ColorRGB(222, 79, 84)
C_GREEN = ColorRGB(121, 220, 154)
C_BLUE = ColorRGB(114, 159, 207)

TODAY_DATE = time.strftime("%Y-%m-%d")
