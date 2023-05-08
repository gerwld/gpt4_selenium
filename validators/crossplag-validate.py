import os
import time
import random
from helpers.createPost import *
from helpers.isPostValid import *
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_RED, C_GREEN
from validators.handlers.crossplagHandler import CrossplagHandler
from validators.handlers.auth import *

MD_STEP_NAME = "_crossplag/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt_improve/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'crossplag-validate: {PATH_TO_PREV_STEP} do not exist.')
else:
    # cтворення директорії якщо не існує
    if not os.path.exists(PATH_TO_CURRENT_STEP):
        os.makedirs(os.path.dirname(PATH_TO_CURRENT_STEP), exist_ok=True)

    # перевірка наявності пройдених постів і фільтрація їх з основного масиву
    prevPosts = os.listdir(os.path.dirname(PATH_TO_PREV_STEP))
    donePosts = os.listdir(os.path.dirname(PATH_TO_CURRENT_STEP))
    if len(donePosts):
        print(
            f'Founded {len(donePosts)} completed posts out of {len(prevPosts)}. Skipping them...')
        prevPosts = list(filter(lambda x: x not in donePosts, prevPosts))

    # якщо є пости, запит на crossplag через хандлер
    if prevPosts and len(prevPosts):
        print(
            f'{C_GREEN}Starting the crossplag-validate [Save directory: {PATH_TO_CURRENT_STEP}]...{C_GREEN.OFF}')
        crossplag = CrossplagHandler(*CROSSPLAG_AUTH)

        for page in prevPosts:
            delay = random.randint(1, 4)
            mdPageContent = ''
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                print(f'{C_GREEN}Working with: {page}...{C_GREEN.OFF}')
                content = pageContent.read()

                # запит на crossplag
                validationResponce = crossplag.interact(post=content)
                # якщо резульат менше 50% звалідуй і збережи, інакше виведи лог
                if validationResponce < 50:
                    print(
                        f'{C_GREEN}Post validated: {page.split(".")[0]}, AI-percent: {validationResponce}%{C_GREEN.OFF}')
                    if isPostValid(content):
                        createPost(page.split('.')[0],
                                   content, delay, MD_STEP_NAME)
                elif validationResponce == 101:
                    print(
                        f'{C_RED}Some error occured with: {page.split(".")[0]}, AI-percent: {validationResponce}%{C_RED.OFF}. Skipping...')
                else:
                    print(
                        f'{C_RED}Post not validated: {page.split(".")[0]}, AI-percent: {validationResponce}%{C_RED.OFF}\n--------------')
                # делей для наступного запиту
                time.sleep(delay)
