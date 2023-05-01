import os
import time
import random
from impovers.handlers.gptHandler import Handler
from helpers.createPost import createPost
from global_context import POSTS_TO_MD, PATH_TO_POSTS, MD_SET_DATE

message = "make post not plagiarized, keep the structure, make it in range between 1000 - 1500 words length, answer just with post: \n"

# отримання постів і прохід по ним, якщо існують
if not os.path.exists(POSTS_TO_MD):
    print(f'POSTS_TO_MD: {POSTS_TO_MD} do not exist in improvers.$')
else:
    # перевірка наявності пройдених постів і фільтрація їх з основного масиву
    htmlPosts = os.listdir(os.path.dirname(POSTS_TO_MD))
    donePosts = os.listdir(os.path.dirname(
        PATH_TO_POSTS + "_gpt/" + MD_SET_DATE + "/"))
    if len(donePosts):
        print(
            f'Founded {len(donePosts)} completed posts out of {len(htmlPosts)}. Skipping them...')
        htmlPosts = list(filter(lambda x: x not in donePosts, htmlPosts))

    # якщо є пости, запит на chatGPT через хандлер
    if htmlPosts and len(htmlPosts):
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
