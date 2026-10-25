# How Original Is My Idea?

Working idea: A user describes an app, startup, or product in normal language. The program will search a vector database of existing product descriptions for conceptually similar ideas, including descriptions that use different words. This initial setup uses only small synthetic smoke-test records.

## Preliminary semantic-search hypotheses

These are hypotheses, not verified retrieval results.

### Test 1

User idea:
"A tool that notices when college students drift to social media during homework and gives them a virtual pet for staying on task."

Expected conceptually similar item:
"A productivity app that blocks distracting websites during timed work sessions and awards collectible creatures for successful sessions."

Why useful: The important concepts are similar, but phrases like "social media", "homework", and "virtual pet" are expressed differently as "distracting websites", "work sessions", and "collectible creatures".

### Test 2

User idea:
"People describe what's sitting in their fridge and get dinner suggestions before their groceries go bad."

Expected conceptually similar item:
"An AI meal planner recommends recipes from ingredients users already have to reduce food waste."

Why useful: The same product concept is described with different language such as "fridge" versus "ingredients", "dinner suggestions" versus "meal planner", and "groceries go bad" versus "food waste".

## Verification status

ChromaDB was initially absent. Verification is now complete; see the dated results below.

## Completed smoke-test verification — 2026-10-24

ChromaDB version: 1.5.9. ONNX Runtime 1.20.1 was needed for this machine; 1.23.2 failed to load a macOS C++ symbol.

First successful process: count before insertion 0, added 10, count after insertion 10. Process exited successfully. Second process: count before insertion 10, added 0, count after insertion 10. Process exited successfully. A separate read verified the saved startup_ideas collection has exactly the 10 expected unique IDs and 10 unique documents. Persistence worked; no duplicates were created.

Both runs returned identical rankings and distances:

| Query | Rank | ID | Product | Distance |
|---|---|---|---|---|
| Test 1 | 1 | focus | Focus Creatures | 1.025099515914917 |
| Test 1 | 2 | pets | Pet Schedule | 1.2263166904449463 |
| Test 1 | 3 | education | Math Mentor | 1.3096671104431152 |
| Test 2 | 1 | meals | Pantry Planner | 1.1571953296661377 |
| Test 2 | 2 | budget | Budget Buddy | 1.4741692543029785 |
| Test 2 | 3 | pets | Pet Schedule | 1.5087820291519165 |
| Nonsense | 1 | education | Math Mentor | 1.8914198875427246 |
| Nonsense | 2 | events | Gather Together | 1.9327669143676758 |
| Nonsense | 3 | pets | Pet Schedule | 1.9415777921676636 |

Both intended semantic matches ranked first. The nonsense query was: "Quantum marshmallow nebula dances inside a purple theorem." Its returned distances were larger than both intended-match distances; no general threshold is established.
