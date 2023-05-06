import os
import time
import random
from bs4 import BeautifulSoup
from global_context import C_RED, PATH_TO_POSTS, MD_SET_DATE
from improvers.handlers.quillbotHandler import QuillbotHandler
from improvers.handlers.auth import QUILLBOT_AUTH
from helpers.createPost import *
from helpers.isPostValid import *

MD_STEP_NAME = "_quillbot/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt_plagiarism/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"

SKIP_PARAGRAPHS_WITH = ["{", "}"]

# отримання постів і прохід по ним, якщо існують
if not os.path.exists(PATH_TO_PREV_STEP):
    print(f'{C_RED}quillBot-parahprase: {PATH_TO_PREV_STEP} do not exist.{C_RED.OFF}')
else:
    os.makedirs(os.path.dirname(PATH_TO_CURRENT_STEP), exist_ok=True)
    prevPosts = list(
        filter(lambda x: x.endswith('.html'), os.listdir(os.path.dirname(PATH_TO_PREV_STEP))))
    donePosts = list(
        filter(lambda x: x.endswith('.html'), os.listdir(os.path.dirname(PATH_TO_CURRENT_STEP))))
    if len(donePosts):
        print(
            f'{C_GREEN}Founded {len(donePosts)} completed posts out of {len(prevPosts)}. Skipping them...{C_GREEN.OFF}')
        prevPosts = list(
            filter(lambda x: x not in donePosts, prevPosts))

    if prevPosts and len(prevPosts):
        # ініціалізуй quillBot
        quillBot = QuillbotHandler(*QUILLBOT_AUTH)

        for page in prevPosts:
            phrasesChanged = 0
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                contentSoup = BeautifulSoup(pageContent, 'html5lib')

                # прохід по всім параграфам
                for p in contentSoup.find_all('p'):
                    parText = str(p.get_text())
                    par_length = len(parText.split(' ')) < 110 and len(
                        parText.split(' ')) > 3

                    if any([x in parText for x in SKIP_PARAGRAPHS_WITH]):
                        print(
                            f'{C_RED}Contains not allowed symbs, skipping:{C_RED.OFF}', parText)
                    # шанс 80% / або перший параграф перевірка на довжину і забороненні символи, якщо все вірно то прохід по параграфу
                    if (random.random() < 0.8 or phrasesChanged == 0) and par_length and not any([x in parText for x in SKIP_PARAGRAPHS_WITH]):
                        newParagraph = quillBot.interact(paragraph=parText)
                        # якщо newParagraph і довжина його слів більше або хочаб дорівнює 70% оригіналу - заміни на неї
                        if newParagraph and len(newParagraph.split(' ')) >= len(str(p.get_text()).split(' ')) * 0.7:
                            print(
                                f'{C_GREEN}Original phrase: {C_GREEN.OFF}{p.get_text()}\n{C_GREEN}To: {C_GREEN.OFF}{newParagraph}\n---------')
                            if p:
                                p.string = newParagraph
                                phrasesChanged += 1
                        time.sleep(1)

                newPost = str(contentSoup.find('article'))
                print(newPost)
                if isPostValid(newPost):
                    # створення поста зі стейджем
                    title = str(page).split('.')[0]
                    createPost(title, newPost, 0, MD_STEP_NAME, phrasesChanged)
