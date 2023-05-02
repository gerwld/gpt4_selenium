import os
import time
import random
from impovers.handlers.gptHandler import Handler
from helpers.createPost import createPost
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_BLUE
from impovers.handlers.auth import GPT_AUTH_TUPPLE, apply_tuple

message = "write a short poem, end it with dot. 20 words max:\n"

MD_STEP_NAME = "_gpt_finished/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'improvers: {PATH_TO_PREV_STEP} do not exist in improvers.$')
else:
    # cтворення нової директорії PATH_TO_CURRENT_STEP якщо не існує
    os.makedirs(os.path.dirname(PATH_TO_CURRENT_STEP), exist_ok=True)

    # прохід по всім статтям і пошук не закінчених
    prevPosts = os.listdir(os.path.dirname(PATH_TO_PREV_STEP))
    notFinishedPosts = []
    for page in prevPosts:
        with open(PATH_TO_PREV_STEP + page) as pageContent:
            content = pageContent.read()
            if (not content or content[-1] != '.' or content[-1] == '!'):
                notFinishedPosts.append(page)

    # якщо немає постів прінт, інакше запит на chatGPT через хандлер
    if not notFinishedPosts or not len(notFinishedPosts):
        print(f'{C_BLUE}Founded {len(notFinishedPosts)} uncompleted posts out of {len(prevPosts)}. Starting...{C_BLUE.OFF}\n' + str(notFinishedPosts))

    else:
        print(f'{C_BLUE}Founded {len(notFinishedPosts)} uncompleted posts out of {len(prevPosts)}. Starting...{C_BLUE.OFF}\n' + str(notFinishedPosts))
        chatgpt = Handler(*GPT_AUTH_TUPPLE)

        for page in notFinishedPosts:
            delay = random.randint(2, 8)
            mdPageContent = ''
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                gptRequest = message + pageContent.read()
                answer = chatgpt.interact(gptRequest)

                # перевірка на ліміт
                if "you've reached our limit of messages per hour" in answer.lower():
                    print('ChatGPT limit reached. Breaking the operation...')
                    break

                # пінгування щоб обійти ліміт і обрив генерації (0 щоб виключити)
                maxPingTries = 0
                startswith = ("sure", "i'm sorry",
                              "thats all", "that's all", 'what')
                while maxPingTries > 0 and (answer[-1] != '.' or answer[-1] != '>' or not answer.lower().startswith(startswith)):
                    print("Starts with", answer.lower(
                    ).startswith(startswith), answer)
                    answer += chatgpt.interact(
                        "keep going")
                    maxPingTries -= 1
                    time.sleep(1)

                # створення поста зі стейджем
                title = str(page).split('.')[0]
                createPost(title, answer, delay, MD_STEP_NAME)

                time.sleep(delay)

        # вихід з сессії
        chatgpt.quit()