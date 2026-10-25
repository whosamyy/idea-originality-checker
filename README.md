# How Original Is My Idea?

## 1. What the App Does and Why I Chose It

My app lets you type in a startup idea and see which Y Combinator companies are the most similar to it. I picked this because I thought it would be interesting to check how original an idea actually is without just searching for the exact same words.

## 2. What Is Stored in the Vector Database

I used a Hugging Face dataset with Y Combinator companies and loaded 1,000 of them into ChromaDB. Each item is one company. I embed the one-liner, tags, and longer description, and keep things like the company name, industry, batch, status, and YC link as metadata. Ideas that users add are also stored in the same collection and marked as user-created.

## 3. How Users Add and Search

Users can add their own idea by giving it a name and description. The description gets embedded and saved in ChromaDB with its own unique ID, so it can be searched right away and is still there after restarting the program.

For searching, the user just describes their idea normally. The app finds the YC companies that are closest in meaning and then shows the closest match, other similar companies, what industries they are in, and some basic distance stats.

## 4. Semantic Search Test Queries

One query I tried was:

“A tool that helps farmers keep track of their cows’ health.”

This matched Cowlar, which makes sense because Cowlar is also about monitoring dairy cows and helping farmers catch health issues. The wording is pretty simple and does not copy the company description, so it still shows that the search is matching the idea rather than just exact words.

Another query I tried was:

“Is there a company that lets small devices stay connected even when there’s no normal cell service?”

This matched Hubble Network near the top. Its description talks about Bluetooth devices, satellites, and working without cellular reception, even though my search describes the idea in a different way.

## 5. How to Obtain and Load the Dataset

I used the datahiveai/ycombinator-companies dataset from Hugging Face. I didn’t include the raw dataset in the GitHub repo, so it needs to be downloaded when setting the project up.

After installing the requirements, run:

python3 load_yc.py

This loads the YC company data into ChromaDB. I use 1,000 companies in the actual project. Running the loader again should not create duplicates.

## 6. Vector Database and Embedding Model

I used ChromaDB for the vector database. The project is currently using ChromaDB 1.5.9 with a persistent local collection, so the data is still there after the program closes.

For embeddings, I used Chroma’s default embedding setup. The model runs locally, so there is no API key needed. The first time it runs, it may need to download the embedding model.

For each company, I embed the company’s one-liner, tags, and longer description. The search returns distances, where a lower distance means the result is closer to the query in the embedding space.

## 7. How to Run the App

First install the dependencies:

python3 -m pip install -r requirements.txt

Then load the YC data if it has not been loaded yet:

python3 load_yc.py

To run the command-line version:

python3 cli.py

I also made a Flask version. To run that:

python3 web_app.py

Then go to:

http://127.0.0.1:5001

in a browser.

## 8. AI Usage

I used Codex for a lot of the coding and debugging in this project. I tried to build it in smaller steps instead of asking it to make the whole thing at once. I first tested ChromaDB with a small set of fake data, then loaded real YC companies, tested the search results, added support for user-submitted ideas, built the analysis part, and then added the CLI and Flask frontend.

I also used ChatGPT mostly for planning the project and helping me figure out what to build next and what to test. I manually checked the search results, database counts, persistence, duplicate handling, and the final app flow as I went. My actual prompts are included in prompt_log.md.