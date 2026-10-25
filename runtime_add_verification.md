# Runtime user-idea insertion verification

Function: `app.add_user_idea(name, description) -> str`.

The function rejects empty names/descriptions, opens the existing persistent `yc_startups` collection, generates a `user:`-prefixed UUID4, and calls `collection.add()` with the description as the document and title/source as metadata. It returns the generated ID. Importing it does not run the smoke-test main function. No interface was added.

Duplicate IDs are not a way to create another item: Chroma add skips an already existing ID rather than adding a distinct record. Reusing a fixed ID could therefore leave later submissions uninserted. UUID4 makes accidental collisions exceedingly unlikely; the user prefix also separates IDs from the `yc:` namespace. This prevents ID collisions, not duplicate descriptions submitted intentionally.

## One development test

Name: Development test — Reef Nursery Monitor

ID: `user:8a87d2f9-c8f8-429e-bc17-c79259264faa`

Metadata: `{"company_name": "Development test — Reef Nursery Monitor", "source": "user"}`

Stored document (the text embedded):

> An underwater camera system watches coral restoration nurseries, detects bleaching and disease in reef fragments, and alerts marine conservation teams when colonies need treatment.

Paraphrased query:

> Help ocean ecologists spot stressed or unhealthy stony sea organisms being regrown, using submerged imaging and automatic warnings.

The key phrases differ: underwater camera versus submerged imaging; coral versus stony sea organisms; bleaching/disease versus stressed/unhealthy; restoration nurseries versus being regrown; alerts versus automatic warnings.

| Check | Insertion process | Fresh process after exit |
|---|---:|---:|
| Collection count | 1000 before; 1001 after | 1001 |
| Added item's rank in top 10 | 1 | 1 |
| Distance | 0.8465203046798706 | 0.8465203046798706 |

The insertion process exited successfully before the verification process started. The fresh process retrieved the exact stored document and metadata by ID and reran the same query. Only one user item was inserted and was retained as persistence evidence.

## Preservation and loader integration

A before-insertion snapshot captured all original 1,000 YC IDs, documents, metadata and embedding vectors. The fresh process compared every original record and found exact equality, including embedding vectors. The only additional ID was the user ID above; no original IDs were missing or overwritten. The collection was not recreated.

`load_yc.py` now distinguishes explicitly marked user records from its fixed 1,000 YC records when checking the shared collection. Its actual rerun inserted 0, kept all 1,000 YC items and the single user idea, and finished with 1001. The separate smoke collection still has 10 items.

Blank name and blank description checks raised the expected ValueError without inserting records. No unexpected errors occurred. Raw snapshots and results are stored under ignored data/.

Files changed: app.py, load_yc.py, prompt_log.md; this verification report was added. The exact user prompt was appended to prompt_log.md. No CLI, frontend, scoring, LLM explanations, deployment or final README was built. Nothing was committed or pushed.
