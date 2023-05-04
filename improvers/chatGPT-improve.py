import os
import time
import random
from improvers.handlers.gptHandler import Handler
from helpers.createPost import *
from helpers.isPostValid import *
from global_context import PATH_TO_POSTS, MD_SET_DATE, C_RED, MAX_PING_TRIES
from improvers.handlers.auth import GPT_AUTH_TUPPLE

message = "change only code examples variables, variable titles, code comments, make them unique to avoid plagiarism, but keep the original text of article. change only code examples. If there is abstract example - like humans, cars, fruits - make them original too. most important - do not change main title and topic, even a symbol of it:\n"

MD_STEP_NAME = "_gpt_improved/"
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
        print(
            f'{C_GREEN}Starting the chatGPT-improve-2 [Save directory: {PATH_TO_CURRENT_STEP}]...{C_GREEN.OFF}')
        chatgpt = Handler(*GPT_AUTH_TUPPLE)

        for page in prevPosts:
            delay = random.randint(1, 3)
            mdPageContent = ''
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                print(f'{C_GREEN}Working with: {page}...{C_GREEN.OFF}')
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
                        f"New request to fix layout, resp. ends with: {newAnswer[len(newAnswer) - 10 :]}")

                    if answer.strip().startswith('<article>') and not newAnswer.strip().startswith('<article>'):
                        answer += newAnswer
                    elif newAnswer.strip().startswith('<article>'):
                        answer = newAnswer
                    maxPingTries -= 1
                    time.sleep(1)

                # перевірка відповіді на валідність
                if isPostValid(answer):
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