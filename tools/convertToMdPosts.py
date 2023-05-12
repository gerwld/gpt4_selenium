import os
import random
from bs4 import BeautifulSoup
from global_context import TITLE_SELECTOR, MD_SET_DATE, MD_PROPS, MD_PREFIX, C_RED, PATH_TO_POSTS
from helpers.trimText import titlecase
from helpers.createMdPost import createMdPost
from datetime import datetime, timedelta


MD_STEP_NAME = "_md/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_unsplash/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# сеттаня дельти відносно start_date
START_DATE = datetime.strptime('2020-01-03', '%Y-%m-%d')
current_date = START_DATE


# отримання постів і прохід по ним, якщо існують
print(PATH_TO_PREV_STEP)
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'{C_RED}convertToMdPosts: {PATH_TO_PREV_STEP} do not exist.{C_RED.OFF}')
else:
    htmlPosts = os.listdir(os.path.dirname(PATH_TO_PREV_STEP))

    if htmlPosts and len(htmlPosts):
        # скільки постів в день "постити", тобто скільки з однією датою додання
        posts_time_reps = 4
        for page in htmlPosts:
            mdPageContent = ''
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                contentSoup = BeautifulSoup(pageContent.read(), 'html5lib')

                # (0) якщо потрібна ітерація - додай день до дельти current_date і відніми ітерацію
                if posts_time_reps > 1:
                    posts_time_reps -= 1
                    # інакше засетай новий ітерейшн геп з рандомом від 2 до 5
                else:
                    posts_time_reps = random.randint(1, 5)
                    current_date += timedelta(days=1)

                POST_DATE = str(current_date).split(' ')[0]

                # (1) формування md по супу
                titleObj = contentSoup.find(TITLE_SELECTOR)
                title = titleObj.get_text()
                desctiption = contentSoup.find('p')
                mdPageContent += f'---\ntitle: {titlecase(title)}\ndescription: {desctiption.get_text().strip()}\ndate: {POST_DATE}\n'

                # (2) додання пропсів в хідер md
                if MD_PROPS and len(MD_PROPS):
                    for prop in MD_PROPS:
                        mdPageContent += prop + '\n'

                mdPageContent += '---\n\n'
                titleObj.extract()

                # (3) формування контенту md (якщо приходить строка сетати її, інакше прохід по супу)
                content = contentSoup if type(contentSoup) == str else contentSoup.find(
                    'body').contents
                for childs in content:
                    mdPageContent += str(childs)

                # (4) cтворення .md
                createMdPost(POST_DATE, title, mdPageContent, MD_PREFIX)

    else:
        print('Invalid htmlPosts in $convertToMdPosts')
