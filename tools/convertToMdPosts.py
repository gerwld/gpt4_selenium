import os
from bs4 import BeautifulSoup
from global_context import POSTS_TO_MD, TITLE_SELECTOR, MD_SET_DATE, MD_PROPS, MD_PREFIX, C_RED
from helpers.trimText import titlecase
from helpers.createMdPost import createMdPost


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(POSTS_TO_MD):
    print(f'{C_RED}convertToMdPosts: {POSTS_TO_MD} do not exist.{C_RED.OFF}')
else:
    htmlPosts = os.listdir(os.path.dirname(POSTS_TO_MD))

    if htmlPosts and len(htmlPosts):
        for page in htmlPosts:
            mdPageContent = ''
            with open(POSTS_TO_MD + page) as pageContent:
                contentSoup = BeautifulSoup(pageContent, 'html5lib')

                # (1) формування md по супу
                titleObj = contentSoup.find(TITLE_SELECTOR)
                title = titleObj.get_text()
                desctiption = contentSoup.find('p')
                mdPageContent += f'---\ntitle: "{titlecase(title)}"\ndescription: "{desctiption.get_text().strip()}"\ndate: {MD_SET_DATE}\n'

                # (2) додання пропсів в хідер md
                if MD_PROPS and len(MD_PROPS):
                    for prop in MD_PROPS:
                        mdPageContent += prop + '\n'

                mdPageContent += '---\n\n'
                titleObj.extract()

                # (3) формування контенту md (якщо приходить строка стетати її, інакше прохід по супу)
                content = type(contentSoup) == str if contentSoup else contentSoup.find(
                    'body').contents
                for childs in content:
                    mdPageContent += str(childs)

                # (4) cтворення .md
                createMdPost(MD_SET_DATE, title, mdPageContent, MD_PREFIX)

    else:
        print('Invalid htmlPosts in $convertToMdPosts')
