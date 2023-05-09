"""Автоматизований і напівавтоматизований прохід по крокам"""
import os
import sys
from global_context import C_RED

# [parse] \ parseNews
if len(sys.argv) > 1 and sys.argv[1] == 'parse':
    with open(os.path.dirname('./tools/') + '/parseNews.py') as f:
        exec(f.read())

# ==== STEPS START ====

# [step1] \ chatGPT-create \ dir: [posts_gpt] \  usability ++
if len(sys.argv) > 1 and sys.argv[1] == 'step1':
    with open(os.path.dirname('./improvers/') + '/chatGPT-create.py') as f:
        exec(f.read())

# [step2] \ chatGPT-code-examples \ dir: [posts_gpt_proj_improve] \ usability +++++
if len(sys.argv) > 1 and sys.argv[1] == 'step2':
    with open(os.path.dirname('./improvers/individual/') + '/chatGPT-code-examples.py') as f:
        exec(f.read())

# [step3] \ chatGPT-paragraphs \ dir: [posts_gpt_paragraphs] \ usability +++++
if len(sys.argv) > 1 and sys.argv[1] == 'step3':
    with open(os.path.dirname('./improvers/') + '/chatGPT-paragraphs.py') as f:
        exec(f.read())

# [step4] \ quillBot-paraphrase \ dir: []
if len(sys.argv) > 1 and sys.argv[1] == 'step4':
    with open(os.path.dirname('./improvers/') + '/quillBot-paraphrase.py') as f:
        exec(f.read())

# [step5] \ chatGPT-detectors \ dir: []
if len(sys.argv) > 1 and sys.argv[1] == 'step5':
    with open(os.path.dirname('./improvers/') + '/chatGPT-detectors.py') as f:
        exec(f.read())

# [step6] \ chatGPT4-improve \ dir: []
if len(sys.argv) > 1 and sys.argv[1] == 'step6':
    with open(os.path.dirname('./improvers/') + '/chatGPT4-improve.py') as f:
        exec(f.read())

# [step7] \ unsplash-add-image \ dir: []
if len(sys.argv) > 1 and sys.argv[1] == 'step7':
    with open(os.path.dirname('./improvers/') + '/unsplash-add-image.py') as f:
        exec(f.read())

# [step8] \ convertToMdPosts \ dir: []
if len(sys.argv) > 1 and sys.argv[1] == 'step8':
    with open(os.path.dirname('./tools/') + '/convertToMdPosts.py') as f:
        exec(f.read())


# ==== STEPS AUTOMATED START (flag: auto) ====

if len(sys.argv) > 1 and sys.argv[1] == 'auto':
    # [step1] \ chatGPT-create \ dir: [posts_gpt] \  usability ++
    # with open(os.path.dirname('./improvers/') + '/chatGPT-create.py') as f:
    #     exec(f.read())

    # [step2] \ chatGPT-code-examples \ dir: [posts_gpt_proj_improve] \ usability +++++
    with open(os.path.dirname('./improvers/individual/') + '/chatGPT-code-examples.py') as f:
        exec(f.read())

    # [step3] \ chatGPT-paragraphs \ dir: [posts_gpt_paragraphs] \ usability +++++
    with open(os.path.dirname('./improvers/') + '/chatGPT-paragraphs.py') as f:
        exec(f.read())

    # [step4] \ quillBot-paraphrase \ dir: []
    with open(os.path.dirname('./improvers/') + '/quillBot-paraphrase.py') as f:
        exec(f.read())

    # [step5] \ chatGPT-detectors \ dir: []
    with open(os.path.dirname('./improvers/') + '/chatGPT-detectors.py') as f:
        exec(f.read())

    # [step6] \ chatGPT4-improve \ dir: []
    with open(os.path.dirname('./improvers/') + '/chatGPT4-improve.py') as f:
        exec(f.read())

    # # [step7] \ crossplag-validate \ dir: []
    # with open(os.path.dirname('./validators/') + '/crossplag-validate.py') as f:
    #     exec(f.read())

    # [step7] \ unsplash-add-image \ dir: []
    with open(os.path.dirname('./improvers/') + '/unsplash-add-image.py') as f:
        exec(f.read())

    # [step8] \ convertToMdPosts \ dir: []
    with open(os.path.dirname('./tools/') + '/convertToMdPosts.py') as f:
        exec(f.read())


# ==== WRONG KEY EXEPTION ====
elif len(sys.argv) > 1:
    print(f'{C_RED}start.py: Wrong argument.{C_RED.OFF}')
