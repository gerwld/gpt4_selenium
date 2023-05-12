"""Створює mdпост і зберігає в PATH_TO_MDPOSTS"""

import os
from global_context import PATH_TO_MDPOSTS, MD_SET_DATE, C_GREEN, C_BLUE
from helpers.onlyAllowed import onlyAllowed

counter = 0


def createMdPost(set_date, title, postData, stage=''):
    # створення назви статті
    if title:
        trimedTitleArr = map(str.lower, onlyAllowed(
            my_string=str(title).strip()).split(' '))
        trimedTitle = set_date + "-" + "-".join(trimedTitleArr)

    # якщо є назва - створити .md-шники в PATH_TO_MDPOSTS зі стейджем
    if trimedTitle and len(trimedTitle):
        pathWithStage = PATH_TO_MDPOSTS + stage + '/' + MD_SET_DATE + '/'

        os.makedirs(os.path.dirname(pathWithStage), exist_ok=True)
        with open(pathWithStage + f'/{trimedTitle}.md', 'w+') as f:
            f.write(str(postData))
            global counter
            counter += 1

        print(f'{C_GREEN}Converted post #{counter} to {C_GREEN.OFF}{C_BLUE}' + PATH_TO_MDPOSTS +
              f'/{trimedTitle}.md{C_BLUE.OFF}, delay: 0s' + '\n--------------')
