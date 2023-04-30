import os
from global_context import PATH_TO_POSTS
from helpers.onlyAllowed import onlyAllowed

counter = 0


def createPost(title, postData, delay):
    # створення назви статті
    if title:
        trimedTitleArr = map(str.lower, onlyAllowed(
            my_string=title).split(' '))
        trimedTitle = "-".join(trimedTitleArr)

    # якщо є назва - створити .html-пейджі
    if trimedTitle and len(trimedTitle):
        os.makedirs(os.path.dirname(PATH_TO_POSTS), exist_ok=True)
        with open(PATH_TO_POSTS + f'/{trimedTitle}.html', 'w+') as f:
            f.write(str(postData))
            global counter
            counter += 1

        print(f'Added post #{counter} to ' + PATH_TO_POSTS +
              f'{trimedTitle}.html, delay: {delay}s' + '\n--------------')
