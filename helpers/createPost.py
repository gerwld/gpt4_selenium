import os
from global_context import PATH_TO_POSTS


def createPost(postData):
    os.makedirs(os.path.dirname(PATH_TO_POSTS), exist_ok=True)
    with open(PATH_TO_POSTS + '/1.md', 'w+') as f:
        f.write(str(postData))
    print(f'Added post to ' + PATH_TO_POSTS)
