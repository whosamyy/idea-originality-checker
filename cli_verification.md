# CLI integration verification

Start from the standalone project directory with `python3 cli.py`.

Files created: cli.py and this verification report. prompt_log.md was updated with the entire attached prompt verbatim. app.py, analysis.py, load_yc.py and dependencies were not changed.

## Flow

1. Analyze a startup idea: prompt for a nonblank description, call analyze_idea(), display the nearest known analog, five YC results with descriptions/metadata/distances, market neighborhood, distance statistics and the unchanged cautious conclusion. User-created matches are displayed separately with overall ranks and IDs.
2. Add a startup idea: prompt for a nonblank name and description, call add_user_idea(), show its generated ID, and ask whether to analyze it now. Yes calls the existing analysis function on its description; no returns to the menu.
3. Quit: print Goodbye and exit. Invalid choices return to the menu. Blank required fields reprompt; invalid yes/no responses reprompt. EOF and Ctrl-C exit gracefully.

Output uses labeled text rather than dictionary dumps. Distances display six decimal places; original full-precision results remain available from analyze_idea(). No retrieval, insertion, or analysis logic was duplicated in the CLI.

## Actual subprocess sessions

Session 1 launched python3 cli.py and supplied invalid and blank menu choices, selected analysis, tested a blank description, then analyzed the cattle query. Closest Known Analog was Cowlar, displayed distance 0.967016. It then selected add, tested a blank name and description, and inserted:

Name: Development test — Avalanche Rescue Mesh

ID: `user:66871cbb-cd1f-4eaa-a620-4c0acde9df9d`

Document: A backcountry safety system links skiers' emergency transceivers into a mesh that locates people buried under snow and alerts nearby rescue teams.

After an invalid yes/no answer it selected yes, analyzed the new item, and displayed:

> Overall rank 1: Development test — Avalanche Rescue Mesh — distance 0.000000

It selected 3 and exited normally. The first process had completely exited before Session 2 launched.

Session 2 launched python3 cli.py, selected analysis, and entered this paraphrase:

> Help mountain responders pinpoint winter sports participants trapped beneath a slide using cooperating radio locators.

The same user item appeared at overall rank 1, displayed distance 1.045027. It selected 3 and exited normally. A further fresh process verified full-precision distance 1.0450271368026733, the stored document and source=user metadata, and count 1002. EOF was also exercised in a separate CLI subprocess and exited cleanly.

## Preservation and issues

Count before insertion: 1001. Count after insertion and restart: 1002. There are exactly 1000 YC companies and two clearly labeled development-test user ideas. The existing reef-monitoring idea remains intact. All 1000 original YC IDs, documents, metadata and embedding vectors were compared to the previously saved baseline and remain exactly unchanged. Only the new user ID was added in this stage. No collection was recreated.

The CLI sessions and input-handling checks passed. The initial test harness kept a parent Chroma client open across child-process database changes; reading embeddings through that stale client raised an internal "Error finding id". Verification was completed using a fresh process and the saved baseline without inserting another idea. No CLI or core-analysis bug was found that required a change.

Transcripts: ignored data/cli_first_session.txt and data/cli_restart_session.txt. Machine-readable verification: ignored data/cli_verification.json. No Flask, frontend, deployment, final README or portfolio integration was added. Nothing was committed or pushed.
