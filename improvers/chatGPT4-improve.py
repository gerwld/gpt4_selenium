"""Обходить AI Content Detectors, методом GPT-4 перефразу"""
import os
import time
import random
from improvers.handlers.gptHandler import ChatGPTHandler
from helpers.createPost import *
from helpers.isPostValid import *
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_RED
from improvers.handlers.auth import GPT_AUTH

# message = "Find last information how GPT model content is detected, and base on that rewrite the above article so that it is not detected as AI content by AI content detectors. Also, make it more human-written, fix any mistakes in it, false info, and improve SEO, keep original structure and length:\n"
message = "fix any mistakes in post, fix false info, make it more human-written, make better SEO, but keep original structure and tags response just with article:\n"

MD_STEP_NAME = "_gpt_improve/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt_detectors/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'{C_RED}chatGPT4-detectors: {PATH_TO_PREV_STEP} do not exist.{C_RED.OFF}')
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
        print(
            f'{C_GREEN}Starting the chatGPT4-improve [Save directory: {PATH_TO_CURRENT_STEP}]...{C_GREEN.OFF}')
        chatgpt = ChatGPTHandler(
            *GPT_AUTH, gpt4=False, should_start_with="<article>")

        for page in prevPosts:
            delay = random.randint(1, 4)
            mdPageContent = ''
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                print(
                    f'{C_GREEN}Working with: {page}...{C_GREEN.OFF}')
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
                maxPingTries = 3
                while maxPingTries > 0 and answer.strip().startswith('<article>') and not answer.strip().endswith('</article>') and not answer.strip().lower().startswith(break_words):
                    newAnswer = chatgpt.interact(
                        'keep going')

                    print(
                        f"{C_GREEN}New request to fix layout, resp. ends with:{C_GREEN.OFF} {newAnswer[len(newAnswer) - 10 :]}")
                    noSpacesAnswer = ''.join(
                        str(answer + newAnswer).strip().split(' '))
                    if answer.strip().startswith('<article>') and not newAnswer.strip().startswith('<article>') and '</article>' not in newAnswer:
                        answer += newAnswer
                    elif newAnswer.strip().startswith('<article>'):
                        answer = newAnswer
                    # якщо починається і закінчується на article
                    elif noSpacesAnswer.startswith('<article>') and noSpacesAnswer.endswith('</article>'):
                        answer += newAnswer
                     # якщо починається і містить закриваючий article
                    elif answer.strip().startswith('<article>') and '</article>' in newAnswer:
                        answer += newAnswer.split("</article>")[
                            0] + "</article>"
                    maxPingTries -= 1
                    time.sleep(1)

                # перевірка відповіді на валідність
                if isPostValid(str(answer).strip()):
                    print(answer)
                    # створення поста зі стейджем
                    title = str(page).split('.')[0]
                    createPost(title, answer, delay, MD_STEP_NAME)

                else:
                    print(answer)
                    print(f'{C_RED}Skipping: {page}...{C_RED.OFF}\n--------------')

                chatgpt.reset_thread()
                time.sleep(delay)

        # вихід з сессії
        chatgpt.quit()
