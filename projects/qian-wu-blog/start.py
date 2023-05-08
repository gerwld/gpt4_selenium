import os
import sys
from global_context import C_RED


# [parse] \ parseNews
if len(sys.argv) > 1 and sys.argv[1] == 'parse':
    with open(os.path.dirname('./tools/') + '/parseNews.py') as f:
        exec(f.read())

# [step0] \ chatGPT-create
if len(sys.argv) > 1 and sys.argv[1] == 'step0':
    with open(os.path.dirname('./improvers/') + '/chatGPT-create.py') as f:
        exec(f.read())

# [step1] \ chatGPT-code-examples
if len(sys.argv) > 1 and sys.argv[1] == 'step1':
    with open(os.path.dirname('./improvers/individual/') + '/chatGPT-code-examples.py') as f:
        exec(f.read())

# [step2] \ chatGPT-paragraphs
if len(sys.argv) > 1 and sys.argv[1] == 'step2':
    with open(os.path.dirname('./improvers/') + '/chatGPT-paragraphs.py') as f:
        exec(f.read())

# [step3] \ chatGPT-reorganize
if len(sys.argv) > 1 and sys.argv[1] == 'step3':
    with open(os.path.dirname('./improvers/') + '/chatGPT-reorganize.py') as f:
        exec(f.read())

# [step4] \ quillBot-paraphrase
if len(sys.argv) > 1 and sys.argv[1] == 'step4':
    with open(os.path.dirname('./improvers/') + '/quillBot-paraphrase.py') as f:
        exec(f.read())

# [step5] \ chatGPT-detectors
if len(sys.argv) > 1 and sys.argv[1] == 'step5':
    with open(os.path.dirname('./improvers/') + '/chatGPT-detectors.py') as f:
        exec(f.read())

# [step6] \ chatGPT4-improve
if len(sys.argv) > 1 and sys.argv[1] == 'step6':
    with open(os.path.dirname('./improvers/') + '/chatGPT4-improve.py') as f:
        exec(f.read())

# [step7] \ crossplag-validate
if len(sys.argv) > 1 and sys.argv[1] == 'step7':
    with open(os.path.dirname('./validators/') + '/crossplag-validate.py') as f:
        exec(f.read())

# [step8] \ unsplash-add-image
if len(sys.argv) > 1 and sys.argv[1] == 'step8':
    with open(os.path.dirname('./improvers/') + '/unsplash-add-image.py') as f:
        exec(f.read())

# [step9] \ convertToMdPosts
if len(sys.argv) > 1 and sys.argv[1] == 'step9':
    with open(os.path.dirname('./tools/') + '/convertToMdPosts.py') as f:
        exec(f.read())
# неправильний аргумент
elif len(sys.argv) > 1:
    print(f'{C_RED}start.py: Wrong argument.{C_RED.OFF}')

# автоматичний режим
else:
    # chatGPT-create
    with open(os.path.dirname('./improvers/') + '/chatGPT-create.py') as f:
        exec(f.read())

    # chatGPT-code-examples
    with open(os.path.dirname('./improvers/individual/') + '/chatGPT-code-examples.py') as f:
        exec(f.read())

    # chatGPT-paragraphs
    with open(os.path.dirname('./improvers/') + '/chatGPT-paragraphs.py') as f:
        exec(f.read())

    # chatGPT-reorganize
    with open(os.path.dirname('./improvers/') + '/chatGPT-reorganize.py') as f:
        exec(f.read())

    # quillBot-paraphrase
    with open(os.path.dirname('./improvers/') + '/quillBot-paraphrase.py') as f:
        exec(f.read())

    # chatGPT-detectors
    with open(os.path.dirname('./improvers/') + '/chatGPT-detectors.py') as f:
        exec(f.read())

    # chatGPT4-improve
    with open(os.path.dirname('./improvers/') + '/chatGPT4-improve.py') as f:
        exec(f.read())

    # crossplag-validate
    with open(os.path.dirname('./validators/') + '/crossplag-validate.py') as f:
        exec(f.read())

    # unsplash-add-image
    with open(os.path.dirname('./improvers/') + '/unsplash-add-image.py') as f:
        exec(f.read())

    # convertToMdPosts
    with open(os.path.dirname('./tools/') + '/convertToMdPosts.py') as f:
        exec(f.read())
