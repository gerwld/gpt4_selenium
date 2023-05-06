import os

with open(os.path.dirname('./improvers/individual/') + '/chatGPT-code-examples.py') as f:
    exec(f.read())
