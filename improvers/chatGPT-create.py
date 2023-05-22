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
from global_context import POSTS_TO_MD, PATH_TO_POSTS, MD_SET_DATE, C_GREEN, C_RED, MAX_PING_TRIES, DEL_CLASS, DEL_PHRASES
from improvers.handlers.auth import GPT_AUTH

message = "completely rephrase the post down below to avoid plagiarism, change the topic, improve code examples, improve SEO, keep structure and tags: \n"
messageGPT4 = 'You are an AI article creation assistant named "PostMachine".\n\
PostMachine MUST create a new post based on the original post to avoid any plagiarism.\n\
PostMachine MUST answer only with an article inside the <article> tag.\n\
The topic of the new post should be similar to the current post topic, but just slightly different.\n\
The structure of the post should be completely different.\n\
The new topic should be interesting, current, based on a real thing or concept, or a programming problem.\n\
The created article should be logical and fact-checked.\n\
The created article should be SEO optimized.\n\
If the created article is based on the installation process with some of the systems, it should be changed to another popular system and the latest version of it.\n\
The created article should resolve a problem.\n\
The main title of the created article should be very short.\n\
The titles of the created article should be very short and logical, but in the style of a personal programming blog.\n\
Every paragraph should be inside a <p> tag, every header, and code example should be inside their corresponding tags, based on W3C HTML Standards.\n\
The created article should be written in a style resembling human authorship, to avoid detection as AI-generated content by AI content detectors.\n\
The created article should have an informative and positive tone of voice, but remain short and simple.\n\
The total word count of the created article should be between 400 and 1200.\n\
The created article must contain at least one of the following phrases: "In my opinion", "Based on", "I think", "I disagree", "I guess", "As we can see".\n\
The created article must have a minimum of two h2 titles.\n\n'

PREFIX = "_gpt/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + PREFIX + MD_SET_DATE + "/"

while True:
    try:
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
                    *GPT_AUTH, should_start_with="<article>", gpt4=False)

                for page in htmlPosts:
                    delay = random.randint(1, 4)
                    mdPageContent = ''
                    with open(POSTS_TO_MD + page) as pageContent:
                        contentReaded = pageContent.read()
                        symbols_length = len(contentReaded)
                        if isPostValid(contentReaded.strip(), isReference=True):
                            print(
                                f'{C_GREEN}Working with: {page}...{C_GREEN.OFF}')
                            gptRequest = messageGPT4 + \
                                str(bs(contentReaded, 'html5lib').find(
                                    'article')).strip()
                            answer = chatgpt.interact(gptRequest)

                        # пінгування щоб обійти ліміт і обрив генерації (0 щоб виключити)
                            break_words = ("sure", "i'm sorry",
                                           "thats all", "that's all", 'what', 'i apologize')
                            # тільки якщо починається з <article>, немає кінця </article> і не починається з break_words
                            maxPingTries = 3
                            while maxPingTries > 0 and answer and answer.strip().startswith('<article>') and not answer.strip().endswith('</article>') and not answer.strip().lower().startswith(break_words):
                                newAnswer = chatgpt.interact('keep going')
                                if isinstance(newAnswer, str) and len(newAnswer):
                                    print(
                                        f"{C_GREEN}New request to fix layout, resp. ends with:{C_GREEN.OFF} {newAnswer[len(newAnswer) - 10 :] if newAnswer else 'null'}")
                                    noSpacesAnswer = ''.join(
                                        str(answer + newAnswer).strip().split(' '))
                                    if newAnswer.strip().lower().startswith(break_words):
                                        answer = ''
                                        maxPingTries = 0
                                        print(
                                            f'{C_RED}Skipping by break_words: {page}...{C_RED.OFF}\n--------------')
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
                                title = str(page).split('.')[0]
                                postSoup = bs(answer, 'html5lib')
                                # трімінг супа
                                for tag in DEL_CLASS:
                                    for match in postSoup.find_all(class_=tag):
                                        match.decompose()
                                # postSoup.find('body').name = 'article'
                                delPhFinalPost = delPhrasesSoup(
                                    postSoup.find('article'), DEL_PHRASES)

                                createPost(title, delPhFinalPost,
                                           delay, PREFIX)

                            else:
                                print(answer)
                                print(
                                    f'{C_RED}Skipping: {page}...{C_RED.OFF}\n--------------')

                            chatgpt.reset_thread()
                            time.sleep(delay)
                        else:
                            print(
                                f'{C_RED}isPostValid reference exeption. Total count: {symbols_length}{C_RED.OFF}')

                # вихід з сессії
                chatgpt.quit()
    except (KeyboardInterrupt):
        print('Stopping task...')
        raise
    except:
        print(f'{C_RED}Re-opening task...{C_RED.OFF}')
        pass
