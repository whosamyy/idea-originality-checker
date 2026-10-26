# Optional Qdrant backend verification — 2026-10-26

## Files and behavior

Created vector_store.py (backend boundary), seed_qdrant.py (manual cloud seeding), verify_qdrant.py (actual integration verifier), tests/test_vector_store.py (offline contracts), pyproject.toml (Vercel entrypoint), and this report. Updated app.py, analysis.py, web_app.py, cli.py, templates/results.html, requirements.txt, .gitignore and prompt_log.md. load_yc.py, local dataset, portfolio and README were not modified.

backend_name() chooses Qdrant only when BOTH QDRANT_URL and QDRANT_API_KEY are nonempty. Otherwise the existing local Chroma collection is used. A configured cloud failure raises a readable error; it does not silently fall back and write to Chroma. add_user_idea(name, description) and analyze_idea(description) keep their public interfaces. Flask uses the same routes for both backends; confirmation lookup also follows backend selection.

Qdrant client uses cloud_inference=True and models.Document(text=..., model="sentence-transformers/all-minilm-l6-v2") for insertion and queries. No local inference runs on that path. A fresh-process import check showed cloud Flask/CLI imports did not load chromadb, onnxruntime or fastembed. qdrant-client version tested: 1.20.0. Existing Chroma dependencies remain in requirements.txt.

## Data model and seeding

Collection: yc_startups. Unnamed vectors: 384 dimensions, cosine metric. An existing incompatible collection is rejected without deletion/recreation. Stable yc:/user: application IDs are preserved in payload. Deterministic UUID5 point IDs satisfy Qdrant’s integer/UUID ID restriction. User application IDs remain user:<UUID4>. Payload contains id, document, metadata and source. YC metadata preserves company_id, company_name, industry, subindustry, batch, status, yc_url and source=yc; user metadata preserves name and source=user.

seed_qdrant.py must be run manually; nothing seeds during Flask startup. It reads exactly the existing 1,000 YC documents/metadata from a temporary copy of chroma_store, skips all local user ideas, and never embeds locally. It creates a source keyword index for filtered cloud searches, uploads missing records in batches of 100 with wait=True, and checks stored payloads on rerun. Existing mismatched payloads stop the seed rather than being overwritten. Deterministic point IDs prevent duplicate records.

Actual seed: uploaded 1,000 YC records; exact YC count 1,000 and total count 1,000. Second seed: added 0; YC count and total stayed 1,000. No local development-test user item was uploaded.

## Actual Chroma regressions

Qdrant variables were absent during local checks. Regression tests ran against a temporary corpus copy so the original store could not be changed by Chroma internal writes on open. Old analysis code from Git HEAD and new analysis produced identical reports for Cowlar/Hubble, apart from the new backend/scoring descriptors. Cowlar remained rank 1, Hubble rank 2. Flask analyze/add/confirmation, existing reef user search and an actual CLI analyze/quit subprocess passed. All insertions for this local regression occurred only in the temporary copy.

Original local count observed: 1006 (1,000 YC plus existing user records). Original chroma_store files were hashed before/after and remained byte-for-byte unchanged. The cloud seeding and integration checks separately verified identical original-store file hashes.

## Actual cloud Flask tests

Credentials were initially absent from the tool shell. After the user authorized sourcing their local setup file, the connection succeeded. Values were used only in the connection/seeding/testing process environments; none were printed, copied into source, or included in this report/prompt log. The original entire task prompt is appended verbatim.

A real Flask process ran on a local test port with both variables inherited. Cowlar, Hubble and meeting-follow-up queries went through POST /analyze; rendered pages showed cosine-distance labels and raw Qdrant scores. The server was stopped completely and a fresh Flask process launched for the persistence check.

| Query | Target | Rank | Raw Qdrant cosine score | Cosine distance (1 − score) |
|---|---|---:|---:|---:|

| Cowlar | Cowlar | 1 | 0.516492 | 0.48350800000000005 |

| Hubble Network | Hubble Network | 2 | 0.47069222 | 0.52930778 |

| Meeting follow-up | Onward | 1 | 0.6156918 | 0.3843082 |

Hubble remains below Doblet, the same ranking problem observed locally; the cloud path does not force or relabel relevance.

Via Flask Add an Idea, inserted **Development test — Cloud Beehive Sound Monitor**, ID `user:92d20baf-ad3c-4a37-bd58-d5d60a3529f9`. It ranked 1 immediately and 1 after Flask restart. Raw score after restart: 1.0; cosine distance: 0.0. This exact-description search is a persistence/integration test, not another independent semantic paraphrase test. The confirmation URL also retrieved its remote source=user payload after restart.

Final remote count: **1001**, consisting of **1000 YC companies and one newly created remote test idea**. The remote development item was retained as persistence evidence. Both owned Flask test processes exited. Raw reports with documents/metadata/scores are under ignored data/qdrant_cloud_verification.json.

## Scoring

Local Chroma retains raw squared L2 distance, lower is closer. Qdrant cosine similarity is higher-is-closer and is preserved as score plus score_metric=cosine_similarity on each cleaned match. Full native results remain under raw_retrieval.*.native_results; raw score arrays remain under scores. The existing lower-is-closer statistics use cosine distance = 1 − score on Qdrant. Reports identify backend and metric explicitly. Flask and CLI show both raw cloud scores and the derived distance with explanatory wording; no cloud value is called a Chroma distance. Do not compare the numeric scales as identical or infer an originality percentage.

## Checks and issues

Six offline contract tests passed: both-variable selection, cloud_inference constructor, idempotent batched seeding/payload preservation, raw-score conversion and no Chroma access on the cloud path, Flask score labels/confirmation, and sanitized cloud errors. Syntax compilation and git diff --check passed. A temporary local regression runner initially needed its import path corrected. The cloud verifier’s normal-query bookkeeping initially looked for the label Meeting follow-up as a company name; corrected the target to Onward and recomputed that rank from the already recorded actual results without another insertion. No production connection, inference, seed or persistence failure occurred after credentials were available.

## Before a future Vercel deployment

pyproject.toml contains [tool.vercel] entrypoint = "web_app:app". web_app.py still exports its existing app variable and python3 web_app.py still works locally. No deployment was attempted.

Before deployment: set both cloud variables in Vercel, use a production-specific dependency/build manifest rather than removing local HW6 dependencies, exclude chroma_store/data/test artifacts from the bundle, arrange static/style.css under public/static/style.css for Vercel static serving, and perform a Vercel build/static-route check. Python packages are not automatically tree-shaken; installing the full Chroma/ONNX dependency set can inflate the bundle even with lazy imports. A deployment-only environment needs Flask and qdrant-client, not Chroma/ONNX/FastEmbed. Keep the current full requirements.txt for local HW6. No package-size or deployed build result is claimed; the standard current Flask Python bundle limit is documented as 500 MB.

Official references: [Qdrant Cloud Inference](https://qdrant.tech/documentation/embeddings/qdrant-cloud-inference/) and [Flask on Vercel](https://vercel.com/docs/frameworks/backend/flask).

Nothing was deployed, committed or pushed. API key values are absent from source, test artifacts, README, prompt log and this report.
