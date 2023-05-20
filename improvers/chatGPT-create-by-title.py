"""Entry-point, створює пост по референсу/ам і повертає максимально сирий пост"""
import os
import time
import random
from bs4 import BeautifulSoup as bs
from helpers.createPost import *
from helpers.isPostValid import *
from helpers.transformTitleToFileName import *
from helpers.delPhrasesSoup import *
from improvers.handlers.gptHandler import ChatGPTHandler
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_GREEN, C_RED, DEL_CLASS, DEL_PHRASES
from improvers.handlers.auth import GPT_AUTH


message = 'Based on artilce title, create a new article.\n\
Created article should be informative, and have logical structure.\n\
Created article should be created as human-written post, to avoid detection as AI content by AI content detectors.\n\
Created article should be written in a style resembling human authorship, to avoid detection as AI-generated content by AI content detectors.\n\
Avoid wrapping anything in triple backticks.\n\
Created article should contain following html structure: be inside <article> tag, use <p> tag for paragraphs, and <h1> <h2> <h3> for titles, <pre> and <code> for code samples.\n\
\n\
Article title: '
PREFIX = "_gpt_bytitle_gpt3/"
PATH_TO_TILES = "./titles/titles.txt"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + PREFIX + MD_SET_DATE + "/"

# отримання заголовків і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_TILES):
    print(f'{C_RED}chatGPT-create-by-title: {PATH_TO_TILES} do not exist.{C_RED.OFF}')
else:
    # cтворення нової директорії PATH_TO_CURRENT_STEP якщо не існує
    os.makedirs(os.path.dirname(PATH_TO_CURRENT_STEP), exist_ok=True)
    # перевірка наявності пройдених постів і фільтрація їх з основного масиву
    with open(PATH_TO_TILES) as titles:
        titlesList = titles.read().split('\n')
        donePosts = os.listdir(os.path.dirname(PATH_TO_CURRENT_STEP))
        if len(donePosts):
            print(
                f'Founded {len(donePosts)} completed posts out of {len(titlesList)}. Skipping them...')
            titlesList = list(
                filter(lambda x: transformTitleToFileName(x, format=".html") not in donePosts, titlesList))

        # якщо є заголовки, запит на chatGPT через хандлер
        if titlesList and len(titlesList):
            chatgpt = ChatGPTHandler(
                *GPT_AUTH, should_start_with="<article>", gpt4=True)

            for title in titlesList:
                delay = random.randint(1, 4)
                mdPageContent = ''
                print(f'{C_GREEN}Working with: {title}...{C_GREEN.OFF}')
                gptRequest = message + str(title).strip()
                answer = chatgpt.interact(gptRequest)

            # пінгування щоб обійти ліміт і обрив генерації (0 щоб виключити)
                break_words = ("sure", "i'm sorry",
                               "thats all", "that's all", 'what')
                # тільки якщо починається з <article>, немає кінця </article> і не починається з break_words
                maxPingTries = 3
                while maxPingTries > 0 and answer and answer.strip().startswith('<article>') and not answer.strip().endswith('</article>') and not answer.strip().lower().startswith(break_words):
                    newAnswer = chatgpt.interact('keep going')
                    if isinstance(newAnswer, str) and len(newAnswer):
                        print(
                            f"{C_GREEN}New request to fix layout, resp. ends with:{C_GREEN.OFF} {newAnswer[len(newAnswer) - 10 :] if newAnswer else 'null'}")
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
                    else:
                        maxPingTries -= 1

                # перевірка відповіді на валідність
                if isPostValid(str(answer).strip()):
                    print(answer)
                    # створення поста зі стейджем
                    title = transformTitleToFileName(title)
                    postSoup = bs(answer, 'html5lib')
                    # трімінг супа
                    for tag in DEL_CLASS:
                        for match in postSoup.find_all(class_=tag):
                            match.decompose()
                    # postSoup.find('body').name = 'article'
                    delPhFinalPost = delPhrasesSoup(
                        postSoup.find('article'), DEL_PHRASES)

                    createPost(title, delPhFinalPost, delay, PREFIX)

                else:
                    print(answer)
                    print(
                        f'{C_RED}Skipping: {title}...{C_RED.OFF}\n--------------')

                chatgpt.reset_thread()
                time.sleep(delay)

            # вихід з сессії
            chatgpt.quit()
