import os
import time
import random
from impovers.handlers.gptHandler import Handler
from helpers.createPost import createPost
from global_context import POSTS_TO_MD

message = "make post not plagiarized, keep the structure, make it at least 1500 words length, answer just with post: \n"

# отримання постів і прохід по ним, якщо існують
if not os.path.exists(POSTS_TO_MD):
    print(f'POSTS_TO_MD: {POSTS_TO_MD} do not exist in improvers.$')
else:
    htmlPosts = os.listdir(os.path.dirname(POSTS_TO_MD))

    if htmlPosts and len(htmlPosts):
        # запит на chatGPT через хандлер
        chatgpt = Handler('patryk.jaworski003@gmail.com', 'aboba12341234')

        for page in htmlPosts:
            delay = random.randint(2, 8)
            mdPageContent = ''
            with open(POSTS_TO_MD + page) as pageContent:
                gptRequest = message + pageContent.read()
                answer = chatgpt.interact(gptRequest)

                # створення поста зі стейджем
                title = str(page).split('.')[0]
                createPost(title, answer, delay, "_gpt")

                time.sleep(delay)

        # вихід з сессії
        chatgpt.quit()
