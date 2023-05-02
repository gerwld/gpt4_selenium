import os
import time
import random
from impovers.handlers.gptHandler import Handler
from helpers.createPost import createPost
from global_context import PATH_TO_POSTS, MD_SET_DATE
from impovers.handlers.auth import GPT_AUTH_TUPPLE, apply_tuple

message = "text down below. make it as html, but don't change the text:\n"

MD_STEP_NAME = "_gpt_1/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'POSTS_TO_MD: {PATH_TO_PREV_STEP} do not exist in improvers.$')
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

    # якщо є пости, запит на chatGPT через хандлер
    if prevPosts and len(prevPosts):
        chatgpt = Handler(*GPT_AUTH_TUPPLE)

        for page in prevPosts:
            delay = random.randint(2, 8)
            mdPageContent = ''
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                gptRequest = message + pageContent.read()
                answer = chatgpt.interact(gptRequest)

                # перевірка на ліміт
                if "you've reached our limit of messages per hour" in answer.lower():
                    print('ChatGPT limit reached. Breaking the operation...')
                    break

                # пінгування щоб обійти ліміт і обрив генерації
                startswith = ("sure", "i'm sorry",
                              "thats all", "that's all", 'what')
                while answer[-1] != '.' and answer[-1] != '>' and not answer.lower().startswith(startswith):
                    answer += chatgpt.interact(
                        "keep going or answer 'Thats all.'")
                    time.sleep(1)

                # створення поста зі стейджем
                title = str(page).split('.')[0]
                createPost(title, answer, delay, MD_STEP_NAME)

                time.sleep(delay)

        # вихід з сессії
        chatgpt.quit()
