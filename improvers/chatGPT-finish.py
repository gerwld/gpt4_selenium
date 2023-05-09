"""Фінальне 'полірування' по змісту"""
import os
import time
import random
from improvers.handlers.gptHandler import ChatGPTHandler
from helpers.createPost import createPost
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_GREEN, C_RED, MAX_PING_TRIES
from improvers.handlers.auth import GPT_AUTH

message = "Finish the post down below, do not change post, just finish it:\n"

MD_STEP_NAME = "_gpt_finished/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'{C_RED}chatGPT-finish: {PATH_TO_PREV_STEP} do not exist.{C_RED.OFF}')

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
        print(f'{C_GREEN}Founded {len(notFinishedPosts)} uncompleted posts out of {len(prevPosts)}. Starting...{C_GREEN.OFF}\n' + str(notFinishedPosts))

    else:
        print(f'{C_GREEN}Founded {len(notFinishedPosts)} uncompleted posts out of {len(prevPosts)}. Starting...{C_GREEN.OFF}\n' + str(notFinishedPosts))
        chatgpt = ChatGPTHandler(
            *GPT_AUTH, should_start_with="<article>")

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
                break_words = ("sure", "i'm sorry",
                               "thats all", "that's all", 'what')
                # тільки якщо починається з <article>, немає кінця </article> і не починається з break_words
                maxPingTries = MAX_PING_TRIES
                while maxPingTries > 0 and answer.strip().startswith('<article>') and not answer.strip().endswith('</article>') and not answer.strip().lower().startswith(break_words):
                    newAnswer = chatgpt.interact('keep going')
                    print(
                        f"{C_GREEN}New request to fix layout, resp. ends with:{C_GREEN.OFF} {newAnswer[len(newAnswer) - 10 :]}")
                    noSpacesAnswer = ''.join(
                        str(answer + newAnswer).strip().split(' '))
                    if answer.strip().startswith('<article>') and not newAnswer.strip().startswith('<article>'):
                        answer += newAnswer
                    elif newAnswer.strip().startswith('<article>'):
                        answer = newAnswer
                    # якщо починається і закінчується на article
                    elif noSpacesAnswer.startswith('<article>') and noSpacesAnswer.endswith('</article>'):
                        answer += newAnswer
                    maxPingTries -= 1
                    time.sleep(1)

                # створення поста зі стейджем
                title = str(page).split('.')[0]
                createPost(title, answer, delay, MD_STEP_NAME)

                time.sleep(delay)

        # вихід з сессії
        chatgpt.quit()
