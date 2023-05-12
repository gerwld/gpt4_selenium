"""Прохід по постам, знаходження підходящої картинки до посту з Unsplash"""
import requests
import os
import time
from improvers.keys.unsplash import *
from bs4 import BeautifulSoup
from global_context import C_RED, PATH_TO_POSTS, MD_SET_DATE

from helpers.createPost import *
from helpers.isPostValid import *

MD_STEP_NAME = "_unsplash/"
PATH_TO_PREV_STEP = PATH_TO_POSTS + "_gpt_improve/" + MD_SET_DATE + "/"
PATH_TO_CURRENT_STEP = PATH_TO_POSTS + MD_STEP_NAME + MD_SET_DATE + "/"


# отримання постів
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

    # і прохід по ним, якщо існують
    if prevPosts and len(prevPosts):
        current_key_index = 0
        for page in prevPosts:
            with open(PATH_TO_PREV_STEP + page) as pageContent:
                contentSoup = BeautifulSoup(pageContent, 'html5lib')
                pageTitle = contentSoup.h1.get_text().strip()
                print(f'{C_GREEN}{pageTitle}{C_GREEN.OFF}')

                # запит на API Unsplash по pageTitle
                try:
                    payload = {'query': pageTitle, 'page': 1,
                               'order_by': 'relevant', 'orientation': 'landscape', 'lang': 'en', 'per_page': len(prevPosts), 'client_id': UNSPLASH_KEYS[current_key_index]}
                    unsplash_request = requests.get(
                        "https://api.unsplash.com/search/photos", payload)
                except requests.exceptions.HTTPError as err:
                    print(f'unsplash-add-image: {err}')

                # якщо реквест пройшов запиши в unsplash_image, інакше повтор
                if unsplash_request.status_code == 200:
                    unsplash_image = unsplash_request.json(
                    )["results"][0]
                else:
                    if current_key_index < len(UNSPLASH_KEYS):
                        current_key_index += 1
                        # повторний запит з іншим key для сторінки ітерації
                        unsplash_request = requests.get(
                            "https://api.unsplash.com/search/photos", payload)
                        if unsplash_request.status_code == 200:
                            unsplash_image = unsplash_request.json()[
                                "results"][0]
                    # якщо останній ключ дохлий - таймаут на минуту
                    else:
                        print(
                            f'{C_RED}Error: {unsplash_request.status_code} on last key. Setting sleep for 1 min...{C_RED.OFF}')
                        time.sleep(60)

                # якщо unsplash_image валідний, апендни його в суп
                if unsplash_image and unsplash_image["urls"]["regular"].startswith('http') and unsplash_image["urls"]["regular"].startswith('http'):
                    new_image = contentSoup.new_tag("img")
                    new_image['src'] = unsplash_image["urls"]["regular"]
                    new_image['alt'] = unsplash_image['alt_description']
                    contentSoup.h1.insert_before(new_image)

                # створення нового посту
                newPost = str(contentSoup.find('article'))
                print(newPost)
                if isPostValid(newPost):
                    # створення поста зі стейджем
                    title = str(page).split('.')[0]
                    createPost(title, newPost, 0, MD_STEP_NAME)
