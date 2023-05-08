"""Додає або віднімає subheadings, в залежності від кількості слів в post"""
import os
import time
import random
from bs4 import BeautifulSoup
from improvers.handlers.gptHandler import ChatGPTHandler
from helpers.createPost import *
from helpers.isPostValid import *
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_RED, MAX_PING_TRIES
from improvers.handlers.auth import GPT_AUTH


count_less = random.randint(1, 2)
count_more = random.randint(2, 3)

message_less = f"remove {count_less} less informative subheading{'s' if count_less > 1 else ''} and it content from the post, keep everything exept it untouched:\n"
message_more = f"add {count_more} more subheading{'s' if count_more > 1 else ''} with content, keep everything exept it untouched:\n"

MD_STEP_NAME = "_gpt_paragraphs/"
PATH_TO_ORIGINAL = PATH_TO_POSTS + "/" + MD_SET_DATE + "/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt_proj_improve/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'{C_RED}chatGPT-paragraphs: {PATH_TO_PREV_STEP} do not exist.{C_RED.OFF}')
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
            f'{C_GREEN}Starting the chatGPT-paragraph... \n[Save directory: {PATH_TO_CURRENT_STEP}]\n[orig:{len(origPosts)}, prev step:{len(prevPosts) + len(donePosts)}, completed:{len(donePosts)}]{C_GREEN.OFF}\n---------')
        chatgpt = ChatGPTHandler(
            *GPT_AUTH, should_start_with="<article>")

        for page in prevPosts:
            delay = random.randint(1, 4)
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                print(f'{C_GREEN}Working with: {page}...{C_GREEN.OFF}')

                # перевірка довжини поста
                post = pageContent.read()
                wordsInPost = len(BeautifulSoup(
                    post, 'html5lib').get_text(' ', strip=True).split(' '))

                # якщо довжина більше 2500 слів, відніми параграфи, інакше додай
                gptRequest = message_more + post
                if wordsInPost > 2500:
                    print(
                        '-'*110 + f'\n{C_GREEN}Words is more than 2500. Removing 1-3 paragraphs. Total words count: {wordsInPost} \n{C_GREEN.OFF}' + '-'*110)
                    gptRequest = message_less + post
                else:
                    print(
                        '-'*110 + f'\n{C_GREEN}Words is less than 2500. Adding 1-2 more. Total words count: {wordsInPost} \n{C_GREEN.OFF}' + '-'*110)

                # запит
                answer = chatgpt.interact(gptRequest)

                # перевірка на ліміт
                if "you've reached our limit of messages" in answer.lower():
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
