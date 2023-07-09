# gpt4_selenium

This project is primarily aimed at developing a bot that utilizes GPT-4 "as it is", with automatization and without using OpenAI API, which is significantly more expensive than $25. Currently it may not be "perfectly shaped", so if you wan't to make some improvements feel free to do it and sumbit pull request. (However, please understand that I may not accept changes that are not beneficial).

![photo_2023-07-10 00 08 23](https://github.com/gerwld/gpt4_selenium/assets/47056812/91aecf98-d9a9-4a9e-99ac-96536e47c064)


## What is working, basically:
- It may be used with GPT3.5 / GPT 4, just set a prop. value to the GPT Handler
- Auto-detection when chat.openai.com "slips" to GPT 3.5, so it doesn't mix up content from 3.5 and 4.
- Autoclicking the "keep going" button / "keep going" message reqest (handling is as less buggy as it can be)
- Binding all answer chunks into one big chunk if the answer is valid, or skipping it.
- Random delay each time, to reduce limit message appearing
- Skipping at the beginning of generation if the generated answer does not start with a chosen value  (\<article\>, etc)
- QuillBot paraphraser to avoid plagiarism or a "computer-ish" tone of voice.

## Init project:

```
git clone git@github.com:gerwld/gpt4_selenium.git && cd gpt4_selenium
pip: -r requirements.txt
```
 
## Tools:
 
### getlinks:

```
python -m tools.getlinks
```

### parseNews:

```
python -m tools.parseNews
```

### convertToMdPosts:

```
python -m tools.convertToMdPosts
```

# To run improvers:

### ChatGpt:

```
python -m improvers.chatGPT
```
