import os
from global_context import PATH_TO_POSTS, MD_SET_DATE
from helpers.onlyAllowed import onlyAllowed

counter = 0


def createPost(title, postData, delay, stage=''):
    # створення назви статті
    if title:
        trimedTitleArr = map(str.lower, onlyAllowed(
            my_string=title).split(' '))
        trimedTitle = "-".join(trimedTitleArr)

    # якщо є назва - створити .html-пейджі
    if trimedTitle and len(trimedTitle):
        pathWithStage = PATH_TO_POSTS + stage + '/' + MD_SET_DATE + '/'

        os.makedirs(os.path.dirname(pathWithStage), exist_ok=True)
        with open(pathWithStage + f'/{trimedTitle}.html', 'w+') as f:
            f.write(str(postData))
            global counter
            counter += 1

        print(f'Added post #{counter} to ' + pathWithStage +
              f'{trimedTitle}.html, delay: {delay}s' + '\n--------------')
