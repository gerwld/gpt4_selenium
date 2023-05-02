import os
from global_context import C_RED, TODAY_DATE
from helpers.isPostValid import *
from helpers.createPost import *

DIRECTORY = './res/posts_gpt_finished/' + TODAY_DATE + "/"

# отримання директорії постів
if not os.path.exists(DIRECTORY):
    print(f'{C_RED}getClearValidPosts: {DIRECTORY} do not exist{C_RED.OFF}')
else:
    clearPosts = os.listdir(os.path.dirname(DIRECTORY))
    # якщо пости існують - прохід по ним
    if clearPosts and len(clearPosts):
        for page in clearPosts:
            with open(DIRECTORY + page) as pageContent:
                # перевірка чи пост валідний і створення посту
                if isPostValid(pageContent.read()):
                    createPost(page.split('.')[0],
                               pageContent.read(), 0, '_valid')
