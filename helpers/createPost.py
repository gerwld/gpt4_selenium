import os
import re
from global_context import PATH_TO_POSTS
from helpers.onlyAllowed import onlyAllowed


def createPost(title, postData, random):
    # створення назви статті
    if title:
        trimedTitleArr = map(str.lower, onlyAllowed(
            my_string=title).split(' '))
        trimedTitle = "-".join(trimedTitleArr)
        print(trimedTitle)

    # якщо є назва - створити .md-шники
    if trimedTitle and len(trimedTitle):
        os.makedirs(os.path.dirname(PATH_TO_POSTS), exist_ok=True)
        with open(PATH_TO_POSTS + f'/{trimedTitle}.md', 'w+') as f:
            f.write(str(postData))
        print(f'Added post to ' + PATH_TO_POSTS + f', delay: {random}s')
