import os
from bs4 import BeautifulSoup
from global_context import C_RED


PATH_TO_SITEMAP = './sitemaps/'
PATH_TO_SAVE_LINKS = './res/sitemaplinks/links.txt'
SHOULD_CONTAIN_STR = ['frontend', 'programming', 'css', 'backend', 'back-end',
                      'front-end', 'javascript', 'ruby', 'apache', 'magento', 'react', 'reactjs', 'spring']
SHOULD_NOT_CONTAIN_STR = ['freelance-jobs']


# отримання постів і прохід по ним, якщо існують
print(PATH_TO_SITEMAP)
if not os.path.exists(PATH_TO_SITEMAP):
    print(f'{C_RED}convertSitemapToPlainLinks: {PATH_TO_SITEMAP} do not exist.{C_RED.OFF}')
else:
    sitemaps = list(filter(lambda x: x.endswith(
        '.xml'), os.listdir(PATH_TO_SITEMAP)))

    if sitemaps and len(sitemaps):
        globalContent = ''
        for page in sitemaps:
            with open(PATH_TO_SITEMAP + page) as pageContent:
                content = pageContent.read()
                # якщо є хочаб одна лінка - пройди по сторінці
                if any(ext in content for ext in SHOULD_CONTAIN_STR):
                    globalContent += str('\n\n' + page + '\n' + '-'*50 + '\n')
                    contentSoup = BeautifulSoup(
                        content, features='lxml')

                    # пошук всіх ссилок і прохід по ним
                    allLinks = contentSoup.find_all('loc')
                    for link in allLinks:
                        parsedLink = link.get_text()

                        if any(ext in parsedLink for ext in SHOULD_CONTAIN_STR) and not any(ext in parsedLink for ext in SHOULD_NOT_CONTAIN_STR):
                            globalContent += str(parsedLink + '\n')

                    # створення нового файлу з усіма лінками
                    if globalContent:
                        count = globalContent.count("http")

                        os.makedirs(os.path.dirname(
                            PATH_TO_SAVE_LINKS), exist_ok=True)
                        with open(PATH_TO_SAVE_LINKS, 'w+') as f:
                            f.write(globalContent)
                        print(
                            f'Successfully added {count} links to ' + PATH_TO_SAVE_LINKS)

    else:
        print('Invalid htmlPosts in $convertSitemapToPlainLinks')
