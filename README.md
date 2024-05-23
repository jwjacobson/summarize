# Summarize: generate abstractive summaries from Project Gutenberg books

### About the app
Summarize is a CLI app written in **Python 3.12**. The CLI uses **Typer** and **Rich** for beautiful rich-text output. The app uses the [Gutendex API](https://gutendex.com/) to retrieve books from Project Gutenberg and the pszemraj's [pegasus-x-large-book-summary](https://huggingface.co/pszemraj/pegasus-x-large-book-summary) LLM to generate abstractive summaries. The user can save summaries to a .txt file or print them to stdout for further piping.

### Installation
Summarize is available as a package on PyPI! You'll need Python 3.12 or later installed.
1. Navigate to the directory where you want to install Summarize.
2. Create a virtual environment: ```python -m venv venv``` (Windows/Linux) or ```python3 -m venv venv``` (Mac).
3. Activate the virtual environment: ```.\venv\Scripts\activate``` (Windows) or ```source venv/bin/activate``` (Linux/Mac).
4. Install summarize: ```pip install summarize-gutenberg```

### Running the app
At present the app retrieves the top 32 books from Project Gutenberg and offers the user a choice among them. Here's how to use it:
1. Make sure your virtual environment is activated.
2. Type ```summarize```
3. Follow the onscreen prompts to create your summary!

### A note on chunks
Summarize works by breaking the source text into chunks of a given number of lines; you can specify how many lines per chunk the program works on. In theory the LLM should work with very large chunks or even entire texts, but experience has shown that a range of 200-800 works best. Please note that the smaller the chunk size, the longer the program will take to run!

### Sample output
[Kafka's *The Metamorphosis*](https://en.wikipedia.org/wiki/The_Metamorphosis), 400 lines per chunk:

> One morning, Samsa wakes from a nightmare and finds himself transformed into a "horrid vermin" in his bed. He is a traveling salesman, and his room is small, but it is comfortable. A picture hangs above the table, showing a woman wearing a hat and a boa. Samsa thinks about how hard it is to be a salesman, how he has to travel all over the world, and how he can never be friendly with anyone. He feels a slight itch on his belly, and pushes himself up onto the bed to lift his head. When he touches the bed, he is overcome by a "cold shudder". He thinks about getting up early, but he knows that other salesmen live a "life of luxury" and that he would get kicked out of his job if he did not have his parents to worry about. He decides that he will pay off his parents' debt, and then he will make the big decision to quit his job. He looks over at the clock, which is ticking past six, and wonders if he could have slept peacefully through the furniture-ratting noise.The next morning, the chief clerk tells Gregor that he has to leave immediately. He tells him that he is in debt to his employer and must look after his parents and sister.The chapter opens with a loud "No" from the family. It's five years later, and the family is still broke. They've lost everything, but they're still able to scrape together enough money to send their sister to the conservatory. The narrator tells us that this is the first time that the family has heard anything positive about their financial situation since the business collapsed five years ago. The family is overjoyed, and they've even gotten used to the idea of having to pay for the expenses of the house. But now that the business is gone, the family can't afford to go back to the good old days. So, they'll have to work.The chapter opens with a description of the situation in which the family finds itself. The family is in the middle of a heated argument when an apple flies through the air and lands on the floor. It is an apple that has been thrown at the family, and it is the apple that is lodged in the flesh of Gregor. The apple is a reminder of the family's reaction to the accident, and the family does not treat the apple as an enemy, but rather as a reminder that the family is patient with its son. The chapter ends with a comparison between the family and a hotel room. The hotel room was a place where the family would gather and talk, but now the family has moved to the bedroom, where they can only talk in the dark.The monster is back, and it's not going to stop until they get rid of him. It's going to take a long time, and they're going to have to live with it for the rest of their lives.

### Planned additional features
There are two major features still to be implemented. The first is a search function allowing you to retrieve any book from Project Gutenberg. The second is a full set of command-line options to control program flow.

### License
Summarize is [free software](https://www.fsf.org/about/what-is-free-software), released under version 3.0 of the GPL. Everyone has the right to use, modify, and distribute Summarize subject to the [stipulations](https://github.com/jwjacobson/summarize/blob/main/LICENSE) of that license. Contributions are welcome!

### Acknowledgments
The overall structure of the app is inspired by Brian Okken's [cards](https://github.com/okken/cards).
The UI and (eventual) search functionality are inspired by [pybites-search](https://github.com/PyBites-Open-Source/search).
The tone of user messages is doubtless inspired by countless hours of [Dungeon Crawl Stone Soup](https://crawl.develz.org/) over the years.
