from parrot import Parrot
import os
import time
import random
from bs4 import BeautifulSoup
from global_context import POSTS_TO_MD, C_RED, PATH_TO_POSTS, MD_SET_DATE
from helpers.trimText import titlecase
from helpers.createMdPost import createMdPost

MD_STEP_NAME = "_parrot_paraphrase/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt_plagiarism/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"

# отримання постів і прохід по ним, якщо існують
if not os.path.exists(POSTS_TO_MD):
    print(f'{C_RED}parrot-paraphrase: {POSTS_TO_MD} do not exist.{C_RED.OFF}')
else:
    os.makedirs(os.path.dirname(PATH_TO_CURRENT_STEP), exist_ok=True)
    prevPosts = list(
        filter(lambda x: x.endswith('.html'), os.listdir(os.path.dirname(PATH_TO_PREV_STEP))))
    donePosts = list(
        filter(lambda x: x.endswith('.html'), os.listdir(os.path.dirname(PATH_TO_CURRENT_STEP))))
    if len(donePosts):
        print(
            f'Founded {len(donePosts)} completed posts out of {len(prevPosts)}. Skipping them...')
        prevPosts = list(
            filter(lambda x: x not in donePosts, prevPosts))

    if prevPosts and len(prevPosts):
        # ініціалізуй Parrot
        parrot = Parrot()

        for page in prevPosts:
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                contentSoup = BeautifulSoup(pageContent, 'html5lib')

                # прохід по всім параграфам
                allParagraphs = contentSoup.find('p')
                if allParagraphs:
                    for p in allParagraphs:
                        parText = str(p.get_text())
                        par_length = len(parText.split(' ')) < 50
                        par_phrases = len(parText.split('.')) <= 2
                        # шанс 30% щоб вернути перефразований параграф
                        if random.random() < 0.8 and par_length and par_phrases:

                            paraphrases = parrot.augment(
                                input_phrase=parText)
                            if paraphrases and paraphrases[0] and paraphrases[0][0]:
                                print(str(parText) + "\n[-----]\n" +
                                      str(paraphrases[0][0]) + "\n---")
                            time.sleep(1)
                            # else:
                            #     print(p)
