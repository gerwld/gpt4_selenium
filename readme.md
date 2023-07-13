# gpt4_selenium

This project is primarily aimed at developing a bot that utilizes GPT-4 "as it is", with automatization and without using OpenAI API, which is significantly more expensive than $25. Currently, it may not be "perfectly shaped", so if you want to make some improvements feel free to contribute. (However, please understand that I may not accept changes that are not beneficial).

![photo_2023-07-10 00 08 23](https://github.com/gerwld/gpt4_selenium/assets/47056812/91aecf98-d9a9-4a9e-99ac-96536e47c064)


## What currently works:
- GPT3.5 / GPT 4, just set a prop. value to the GPT Handler
- Auto-detection when chat.openai.com "slips" to GPT 3.5, so it doesn't mix up content from 3.5 and 4.
- Auto-clicking the "keep going" button / "keep going" message request (handling is as less buggy as it can be)
- Binding all answer chunks into one big chunk if the answer is valid, or skipping it.
- Random delay each time, to reduce limit messages appearing.
- Skipping at the beginning of generation if the generated answer does not start with a chosen value (\<article\>, any preferred).
- QuillBot paraphraser to avoid AI content detection, plagiarism and a "computer-ish" tone of voice.

## FAQ:
### Why should I create an HTML post first? Isn't it more efficient to make it markdown at the beginning?
It may look logical, but the simple answer is no. Because even GPT-4 is often delusional, and the main idea is to provide some "anchors", such as tags to validate that the current post content is valid. But you may try.

### Are there any principles to make posts better?
The more laconic and concrete the request is, the more is possible to get a good answer. Also, keep in mind that all history that the selected chat have is basically submitted every time again, which increases the entropy of the request, and can cause delusion. Anyways, somehow even with a good query GPT "goes crazy", so it's a good practice to check the post before publishing it.

<br><br>

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

<br>

## To run improvers:

### ChatGpt:

```
python -m improvers.chatGPT
```

