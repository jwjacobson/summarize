# Summarize: generate summaries from Project Gutenberg books

### About the app
Summarize is a CLI app written in **Python 3.12.1**. The CLI uses **Typer** and **Rich** for beautiful rich-text output. The app uses the [Gutendex API]() to retrieve books from Project Gutenberg and the pszemraj/pegasus-x-large-book-summary LLM to generate summaries.

### Local installation
Eventually Summarize will be packaged on pypi, but for now you can install it by cloning from Github. You'll need Python 3.12 or later installed.
1. [Clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
2. Navigate to the 'summarize' directory.
3. Create a virtual environment ```python -m venv venv''' (Windows/Linux) or ```python3 -m venv venv``` (Mac).
4. Activate the virtual environment ```.\venv\Scripts\activate``` (Windows) or ```source venv/bin/activate```
5. Install the necessary packages: ```pip install -r requirements.txt``` (There is also a requirements.in if you prefer to use pip-tools)

### Running the app
At present the app retrieves the top 32 books from Project Gutenberg and offers the user a choice among them. Here's how to use it:
1. Make sure your virtual environment is activated.
2. Run ```python src/summarize/__main__.py```
3. Follow the onscreen prompts to create your summary!

### A note on chunks
Summarize works by breaking the source text into chunks of a given number of lines; you can specify how many lines per chunk the program works on. In theory the LLM should work with very large chunks, but experience has shown that a range of 200-800 works best. Please note that the smaller the chunk size, the longer the program will take to run!

### License
Summarize is [free software](https://www.fsf.org/about/what-is-free-software), released under version 3.0 of the GPL. Everyone has the right to use, modify, and distribute Summarize subject to the [stipulations](https://github.com/jwjacobson/summarize/blob/main/LICENSE) of that license.
