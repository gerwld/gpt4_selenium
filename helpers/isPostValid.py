from global_context import MIN_WORDS_LIMIT, MAX_WORDS_LIMIT


# перевіряє чи пост відповідає заданим критеріям. якщо ні - повертає False
def isPostValid(post):
    if post and str(post):
        wordsCount = post if len(
            list(filter(lambda x: len(x), str(post).split(' ')))) else 0
        return len(wordsCount) > MIN_WORDS_LIMIT and len(wordsCount) < MAX_WORDS_LIMIT and post.strip().startswith('<article>') and post.strip().endswith('</article>')
    return False
