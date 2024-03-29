"""Створює пост і зберігає в PATH_TO_POSTS"""
import os
import random
import time
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_BLUE, C_GREEN, C_RED
from helpers.onlyAllowed import onlyAllowed

counter = 0


def createPost(title, postData, delay, stage='/', changed=0, isTimeout=True):
    # створення назви статті
    if title:
        trimedTitleArr = map(str.lower, onlyAllowed(
            my_string=title).split(' '))
        trimedTitle = "-".join(filter(lambda x: len(x), trimedTitleArr))

    # якщо є назва - створити .html-пейджі
    if trimedTitle and len(trimedTitle):
        pathWithStage = PATH_TO_POSTS + stage + MD_SET_DATE

        # cтворення директорії якщо не існує
        if not os.path.exists(pathWithStage):
            os.makedirs(pathWithStage, exist_ok=True)

        os.makedirs(os.path.dirname(pathWithStage), exist_ok=True)
        with open(pathWithStage + f'/{trimedTitle}.html', 'w+') as f:
            f.write(str(postData))
            global counter
            counter += 1

        changedParagraphs = f' changed paragraphs: {changed},' if (
            changed > 0) else ''

        print(f'{C_GREEN}Added post #{counter} to {C_GREEN.OFF}{C_BLUE}' + pathWithStage +
              f'/{trimedTitle}.html{C_BLUE.OFF},{changedParagraphs} delay: {delay}s' + '\n--------------')

        if counter % 240 == 0 and isTimeout:
            timeout = random.randint(1, 6)
            print(
                f'{C_RED}Setting timeout to {timeout} minutes, to avoid block by IP{C_RED.OFF}')
            time.sleep(timeout*60)
