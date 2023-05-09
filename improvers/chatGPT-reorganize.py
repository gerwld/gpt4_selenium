"""Реорганізовує subheadings в кожному пості, залишаючи зміст"""
import os
import time
import random
from improvers.handlers.gptHandler import ChatGPTHandler
from helpers.createPost import *
from helpers.isPostValid import *
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_RED, MAX_PING_TRIES
from improvers.handlers.auth import GPT_AUTH


message = "improve subheadings titles SEO, slightly improve explanations. make it human-written and try to keep original words length: \n"

MD_STEP_NAME = "_gpt_reorganize/"
PATH_TO_ORIGINAL = PATH_TO_POSTS + "/" + MD_SET_DATE + "/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt_paragraphs/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'{C_RED}chatGPT4-reorganize: {PATH_TO_PREV_STEP} do not exist.{C_RED.OFF}')
else:
    # cтворення директорії якщо не існує
    if not os.path.exists(PATH_TO_CURRENT_STEP):
        os.makedirs(os.path.dirname(PATH_TO_CURRENT_STEP), exist_ok=True)

    # перевірка наявності пройдених постів і фільтрація їх з основного масиву
    origPosts = os.listdir(os.path.dirname(PATH_TO_ORIGINAL))
    prevPosts = os.listdir(os.path.dirname(PATH_TO_PREV_STEP))
    donePosts = os.listdir(os.path.dirname(PATH_TO_CURRENT_STEP))
    if len(donePosts):
        prevPosts = list(
            filter(lambda x: x not in donePosts and x in origPosts, prevPosts))

    # якщо є пости, запит на chatGPT через хандлер
    if prevPosts and len(prevPosts):
        print(
            f'{C_GREEN}Starting the chatGPT-reorganize... \n[Save directory: {PATH_TO_CURRENT_STEP}]\n[orig:{len(origPosts)}, prev step:{len(prevPosts) + len(donePosts)}, completed:{len(donePosts)}]{C_GREEN.OFF}\n---------')
        chatgpt = ChatGPTHandler(
            *GPT_AUTH, should_start_with="<article>")

        for page in prevPosts:
            delay = random.randint(1, 4)
            with open(PATH_TO_PREV_STEP + page) as prevStepPageContent:
                with open(PATH_TO_ORIGINAL + page) as originalContent:
                    print(f'{C_GREEN}Working with: {page}...{C_GREEN.OFF}')
                    # запит на chatgpt
                    gptRequest = message + originalContent.read()
                    answer = chatgpt.interact(gptRequest)

                    # пінгування щоб обійти ліміт і обрив генерації (0 щоб виключити)
                    break_words = ("sure", "i'm sorry",
                                   "thats all", "that's all", 'what')
                    # тільки якщо починається з <article>, немає кінця </article> і не починається з break_words
                    maxPingTries = MAX_PING_TRIES
                    while maxPingTries > 0 and answer.strip().startswith('<article>') and not answer.strip().endswith('</article>') and not answer.strip().lower().startswith(break_words):
                        newAnswer = chatgpt.interact('keep going')
                        print(
                            f"New request to fix layout, resp. ends with: {newAnswer[len(newAnswer) - 10 :]}")

                        if answer.strip().startswith('<article>') and not newAnswer.strip().startswith('<article>'):
                            answer += newAnswer
                        elif newAnswer.strip().startswith('<article>'):
                            answer = newAnswer
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
                        print(
                            f'{C_RED}Skipping: {page}...{C_RED.OFF}\n--------------')

                    chatgpt.reset_thread()
                    time.sleep(delay)

        # вихід з сессії
        chatgpt.quit()
