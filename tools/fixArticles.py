import os
import random
from bs4 import BeautifulSoup
from global_context import TITLE_SELECTOR, MD_SET_DATE, C_RED, PATH_TO_POSTS, MD_SET_DATE
from helpers.trimText import titlecase
from helpers.createPost import *

MD_STEP_NAME = '_fixed/'
PATH_TO_PREV_STEP = PATH_TO_POSTS + "/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
print(PATH_TO_PREV_STEP)
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'{C_RED}convertToMdPosts: {PATH_TO_PREV_STEP} do not exist.{C_RED.OFF}')
else:
    htmlPosts = os.listdir(os.path.dirname(PATH_TO_PREV_STEP))

    if htmlPosts and len(htmlPosts):
        for page in htmlPosts:
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                contentSoup = BeautifulSoup(pageContent.read(), 'html5lib')
                article = contentSoup.find('article')
                source = contentSoup.find('del')
                postTitle = contentSoup.find(
                    TITLE_SELECTOR).get_text().strip()

            # якщо в контенті немає тайтлу але є в супі - додай в суп
            if not article.find(TITLE_SELECTOR) and len(postTitle):
                titleTag = contentSoup.new_tag('h1')
                titleTag.string = postTitle
                if article.p:
                    article.p.insert_before(titleTag)
                    print("Inserted title inside article.")
                    # (4) cтворення .md
                    createPost(page.split('.')[
                        0], str(source) + str(article), 0, MD_STEP_NAME, isTimeout=False)
            elif article.p and article.h1:
                print("Post is valid.")
                createPost(page.split('.')[
                    0], str(source) + str(article), 0, MD_STEP_NAME, isTimeout=False)

    else:
        print('Invalid htmlPosts in $convertToMdPosts')
