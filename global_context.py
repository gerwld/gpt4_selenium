
import time
from colorist import ColorRGB

CURRENT_PROJECT = 'qian-wu-blog'

PATH_TO_LINKS = './res/sitemaplinks/links.txt'
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
MIN_WORDS_LIMIT = 250
MAX_WORDS_LIMIT = 9000

# скільки разів пінгувати при обриві відповіді chatGPT. Оптимально - від 2 до 4, щоб виключити 0
MAX_PING_TRIES = 3


TITLE_SELECTOR = 'h1'

DEL_PHRASES = [
    "Thank you for reading this article.",
    "Thank you for reading this article!",
    "Thank you for reading this article!!",
    "Thank you for reading this article",
    "Thank you for reading this blog.",
    "Thank you for reading this blog!",
    "Thank you for reading this blog!!",
    "Thank you for reading this blog",
    "Thank you.",
    "Thank you",
    "Thank you.",
    "<p>Press&lt;Enter&gt;. </p>",
    "<p>Press Enter\&gt;. </p>",
    "<p>Press Enter&gt;. </p>",
    "<p>Press&lt;Enter&gt;. </p>",
    "<p>Press\&lt;Enter\&gt;. </p>",
]

DEL_CLASS = [
    "itemhead",
]

DEL_TAGS = [
    "h6",
    "u",
    "script",
    "footer",
    "iframe",
    "img",
    "bloquote",
    "figure",
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
    "a",
    "span",
    "article",
    "section",
    "header",
    "html",
    "head",
    "body",
    "main",
    "div",
    "strong",
    "tt",
    "i",]

MD_PROPS = ['layout: post']

C_RED = ColorRGB(222, 79, 84)
C_GREEN = ColorRGB(121, 220, 154)
C_BLUE = ColorRGB(114, 159, 207)

TODAY_DATE = time.strftime("%Y-%m-%d")
