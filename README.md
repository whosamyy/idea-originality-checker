# How Original Is My Idea?

## 1. What the App Does and Why I Chose It

My app lets you type in a startup idea and see which Y Combinator companies are the most similar to it. I picked this because I thought it would be interesting to check how original an idea is without just searching for companies that use the exact same words.

Instead of doing a normal keyword search, the app compares the meaning of the idea to descriptions of existing YC companies.

## 2. What Is Stored in the Vector Database

I used the datahiveai/ycombinator-companies dataset from Hugging Face and loaded 1,000 YC companies into the database.

Each item represents one company. I embed its one-liner, tags, and longer description, and store things like the company name, industry, batch, status, and YC link as metadata.

User-added ideas are stored in the same collection and marked as user-created.

## 3. How Users Add and Search

Users can add an idea by entering a name and description. The description is embedded and saved with a unique ID, so it can be searched immediately and still exists after restarting the program.

For searching, the user just describes their idea normally. The app finds companies that are closest in meaning and shows the closest match, other similar companies, their industries, and some distance information.

It also gives a basic competitive landscape instead of only showing raw search results.

## 4. Semantic Search Test Queries

One query I tested was:

"A device worn by cattle that warns ranchers when an animal may be ill or ready to breed."

This returned Cowlar as the closest match. Cowlar is also focused on monitoring dairy cows and detecting health and reproduction issues, even though the wording is different.

Another query was:

"Let small wireless gadgets send updates from remote areas where phones have no signal, through equipment orbiting Earth."

This returned Hubble Network near the top. Its description talks about Bluetooth devices, satellites, and working without cellular reception.

## 5. How to Obtain and Load the Dataset

Dataset:

datahiveai/ycombinator-companies

https://huggingface.co/datasets/datahiveai/ycombinator-companies

Install the requirements:

python3 -m pip install -r requirements.txt

Then load the data:

python3 load_yc.py

This loads 1,000 YC companies into ChromaDB. Running it again should not create duplicates.

## 6. Vector Database and Embedding Model

The local HW6 version uses ChromaDB 1.5.9 with persistent storage.

For embeddings, I use Chroma's default all-MiniLM-L6-v2 model. The company one-liner, tags, and description are embedded together.

A smaller Chroma distance means two results are closer in the embedding space, but I do not treat the distance as an originality percentage.

For the public Vercel deployment, I use Qdrant Cloud instead of local Chroma storage. The local version still defaults to ChromaDB.

## 7. How to Run the App

Install dependencies:

python3 -m pip install -r requirements.txt

Load the YC data if needed:

python3 load_yc.py

Run the CLI:

python3 cli.py

Or run the Flask version:

python3 web_app.py

Then open:

http://127.0.0.1:5001

Live demo:

https://idea-originality-checker.vercel.app

## 8. AI Usage

I used Codex for coding and debugging, and ChatGPT mostly for planning what to build next and writing prompts.

I built the project in smaller steps: first testing ChromaDB with fake data, then loading real YC companies, adding user ideas, building the analysis, and finally making the CLI and Flask frontend.

I manually checked the search results, database counts, persistence, duplicate handling, and the final app flow.

My actual prompts are included in prompt_log.md.