import time
from improvers.handlers.quillbotHandler import QuillbotHandler


quillbot = QuillbotHandler()

while True:
    result = quillbot.interact(paragraph="Lets test that shi")
    print(result)
    time.sleep(3)
