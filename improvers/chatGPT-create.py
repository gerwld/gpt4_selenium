"""Entry-point, створює пост по референсу/ам і повертає максимально сирий пост"""
import os
import time
import random
from helpers.createPost import *
from helpers.isPostValid import *
from improvers.handlers.gptHandler import ChatGPTHandler
from global_context import POSTS_TO_MD, PATH_TO_POSTS, MD_SET_DATE, C_GREEN, C_RED, MAX_PING_TRIES
from improvers.handlers.auth import GPT_AUTH

message = "completely rephrase the post down below to avoid plagiarism, improve code examples, improve SEO, keep structure and tags: \n"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + "_gpt/" + MD_SET_DATE + "/"


# отримання постів і прохід по ним, якщо існують
if not os.path.exists(POSTS_TO_MD):
    print(f'{C_RED}chatGPT-create: {POSTS_TO_MD} do not exist.{C_RED.OFF}')
else:
    # cтворення нової директорії PATH_TO_CURRENT_STEP якщо не існує
    os.makedirs(os.path.dirname(PATH_TO_CURRENT_STEP), exist_ok=True)
    # перевірка наявності пройдених постів і фільтрація їх з основного масиву
    htmlPosts = os.listdir(os.path.dirname(POSTS_TO_MD))
    donePosts = os.listdir(os.path.dirname(PATH_TO_CURRENT_STEP))
    if len(donePosts):
        print(
            f'Founded {len(donePosts)} completed posts out of {len(htmlPosts)}. Skipping them...')
        htmlPosts = list(
            filter(lambda x: x not in donePosts and x and x.endswith('.html'), htmlPosts))

    # якщо є пости, запит на chatGPT через хандлер
    if htmlPosts and len(htmlPosts):
        chatgpt = ChatGPTHandler(
            *GPT_AUTH, should_start_with="<article>")

        for page in htmlPosts:
            delay = random.randint(1, 4)
            mdPageContent = ''
            with open(POSTS_TO_MD + page) as pageContent:
                print(f'{C_GREEN}Working with: {page}...{C_GREEN.OFF}')
                gptRequest = message + pageContent.read()
                answer = chatgpt.interact(gptRequest)

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

                # перевірка відповіді на валідність
                if isPostValid(str(answer).strip()):
                    print(answer)
                    # створення поста зі стейджем
                    title = str(page).split('.')[0]
                    createPost(title, answer, delay, "_gpt/")

                else:
                    print(answer)
                    print(f'{C_RED}Skipping: {page}...{C_RED.OFF}\n--------------')

                chatgpt.reset_thread()
                time.sleep(delay)

        # вихід з сессії
        chatgpt.quit()
