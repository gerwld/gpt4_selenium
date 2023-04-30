import os
from global_context import PATH_TO_MDPOSTS
from helpers.onlyAllowed import onlyAllowed

counter = 0


def createMdPost(set_date, title, postData):
    # створення назви статті
    if title:
        trimedTitleArr = map(str.lower, onlyAllowed(
            my_string=str(title)).split(' '))
        trimedTitle = set_date + "-" + "-".join(trimedTitleArr)[:-1]

    # якщо є назва - створити .md-шники
    if trimedTitle and len(trimedTitle):
        os.makedirs(os.path.dirname(PATH_TO_MDPOSTS), exist_ok=True)
        with open(PATH_TO_MDPOSTS + f'/{trimedTitle}.md', 'w+') as f:
            f.write(str(postData))
            global counter
            counter += 1

        print(f'Converted post #{counter} to ' + PATH_TO_MDPOSTS +
              f'{trimedTitle}.md, delay: 0s' + '\n--------------')
