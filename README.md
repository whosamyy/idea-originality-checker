# How Original Is My Idea?

## 1. What the App Does and Why I Chose It

My app lets you type in a startup idea and see which Y Combinator companies are the most similar to it. I picked this because I thought it would be interesting to compare ideas by meaning instead of just searching for the same words.

## 2. What Is Stored in the Vector Database

I used the [datahiveai/ycombinator-companies dataset](https://huggingface.co/datasets/datahiveai/ycombinator-companies) from Hugging Face and loaded 1,000 YC companies.

Each item represents one company. I embed its one-liner, tags, and longer description, and store the company name, industry, subindustry, batch, status, ID, and YC link as metadata.

User-added ideas are stored in the same collection and marked as user-created.

## 3. How Users Add and Search

Users add an idea by entering a name and description. The description is embedded and saved with a unique ID, so it can be searched immediately and still exists after restarting the program.

For searching, users describe their idea normally. The app shows the closest semantic match, other nearby companies, their industries, and distance information. This gives a basic competitive landscape, but the results are not automatically confirmed competitors.

## 4. Semantic Search Test Queries

**Test 1:**

> A device worn by cattle that warns ranchers when an animal may be ill or ready to breed.

Cowlar ranked #1. It monitors dairy cows and detects health and reproduction issues. Words like “cattle,” “ill,” and “breed” express similar meanings to “cows,” “diseases,” and “reproduction.” Exact keyword matching could miss those connections.

**Test 2:**

> Let small wireless gadgets send updates from remote areas where phones have no signal, through equipment orbiting Earth.

Hubble Network ranked #2. Its description uses “Bluetooth devices,” “satellites,” and “without cellular reception” instead of the query’s wording. This is why keyword matching could be less reliable. I did not run a separate keyword-search comparison.

## 5. How to Obtain and Load the Dataset

Use Python 3.13 and run these commands from the project folder. Keep `QDRANT_URL` and `QDRANT_API_KEY` unset for local Chroma mode.

```bash
python3 -m pip install -r requirements.txt
mkdir -p data
curl -L --fail "https://huggingface.co/datasets/datahiveai/ycombinator-companies/resolve/main/yc-companies.csv" -o data/yc-companies.csv
python3 app.py
python3 load_yc.py
```

Run `app.py` first to create the separate smoke-test collection and download the embedding model. Then `load_yc.py` loads 1,000 real companies into `yc_startups`. Re-running the loader skips existing records. The raw data and local database are ignored by Git.

## 6. Vector Database and Embedding Model

I tested the local version with ChromaDB 1.5.9 and its default all-MiniLM-L6-v2 embedding model. It saves data in `chroma_store/`. The first run needs internet to download the model; later local searches use the cached copy.

Lower Chroma distances mean closer embeddings, not an originality percentage. The public app uses Qdrant Cloud with cloud embeddings when both `QDRANT_URL` and `QDRANT_API_KEY` are set. Its cosine scores and distances are labeled separately from Chroma’s.

## 7. How to Run the App

After the setup above, run the CLI:

```bash
python3 cli.py
```

Or start Flask:

```bash
python3 web_app.py
```

Open [http://127.0.0.1:5001](http://127.0.0.1:5001) and keep the terminal running.

[Live demo](https://idea-originality-checker.vercel.app)

## 8. AI Usage

I used Codex for coding, debugging, and README edits, and ChatGPT mostly for planning what to build next and writing prompts.

I built the project in smaller steps, from testing Chroma with sample data to loading real companies and making the CLI and Flask frontend. I checked search results, counts, persistence, duplicate handling, and the app flow. My prompts are in [prompt_log.md](prompt_log.md).
