from global_context import MIN_WORDS_LIMIT, MAX_WORDS_LIMIT


# перевіряє чи пост відповідає заданим критеріям. якщо ні - повертає False
def isPostValid(post, isReference=False):
    if post and str(post):
        wordsCount = len(str(post).split(' ')) if post else 0
        print(f'wordsCount: {wordsCount}')
        if isReference:
            return wordsCount > MIN_WORDS_LIMIT and wordsCount < MAX_WORDS_LIMIT and '<article>' in post.strip() and post.strip().endswith('</article>')

        return wordsCount > MIN_WORDS_LIMIT and wordsCount < MAX_WORDS_LIMIT and post.strip().startswith('<article>') and post.strip().endswith('</article>')
    return False
