# Daily Tasks

## 1. Quiz on last session's contents

- How are LLMs different from machine learning models and models that came before them?
- What is meant by the statement "LLMs are stateless" and what does it imply for how we send items to LLMs?
- What is the context of an LLM?
- What is an embedding, and what are the advantages of using embeddings?
- Are fine-tuning and reinforcement learning parts of LLM pre-training?
- What is the difference between RAG and agentic RAG?
- What is a prompt injection, and what is the difference between a prompt injection and a jailbreak?
- What are some simple ways of avoiding hallucinations?

---


## 2. Claude Code practise

1. Open Claude Code
2. Check model and context using `/model` and `/context`
3. Ask it to give you a summary of what is in the folder
4. Close Claude Code and then resume the previous conversation
5. Then Claude Code should perform the task of extracting metadata from 10 PDFs in the `ifoa_downloads/` folder, closely following `ifoa_downloads/prompt.txt`

---

## 3. Bash practise task

These instructions will help you to practise your Bash skills. Replace X with your name.

1. Display your current folder, then list all its files using the detailed view.
2. Create a folder called `bash_practice` and change into it.
3. Open the current folder in VS Code using `code .`
4. Create a folder called `tmp`.
5. Use `touch` to create `tmp/hello.txt`, then use `echo` and `>` to add "Hello, my name is X".
6. Display the contents of `tmp/hello.txt`.
7. Copy it to a new file called `tmp/hello2.txt`.
8. Append "and I am an actuary" to `tmp/hello2.txt` using `echo` and `>>`.
9. Use `grep -n` to search for "actuary" in `tmp/hello2.txt`.
10. Use `nano` to create `notes.txt`, add a short message, save it and exit.
11. Rename `tmp/hello2.txt` to `tmp/profile.txt`; enter `tmp`, then use `cd -` to return.
12. Check your location, delete `hello.txt` and `profile.txt` using `rm`, then list `tmp` to confirm.

---

## 4. Langchain API

Working in `main.ipynb` or `main_colab.ipynb`:
- Fetch API key from Open AI Portal https://platform.openai.com/api-keys
- Single prompt response
- Single prompt response (batch)
- Chatting with the API (with no memory)
- Chatting with the API (with memory)



