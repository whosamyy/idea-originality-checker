# Final Vercel preparation — 2026-10-26

- Entrypoint remains `web_app:app` in `pyproject.toml`. The top-level value is a Flask instance; importing it does not start the development server.
- Production manifest: `[project].dependencies = ["Flask==3.1.3", "qdrant-client==1.20.0"]`, Python `>=3.13,<3.14`, `[tool.uv] package = false`.
- Vercel's current Python manifest loader selects native pyproject metadata before requirements.txt. The full root requirements.txt is unchanged for local HW6 (`python3 -m pip install -r requirements.txt`). No custom Install Command is needed; leave the Vercel install override unset.
- Qdrant's required transitive packages (including NumPy, HTTP/gRPC and Pydantic packages) are still necessary. No FastEmbed extras, Chroma, ONNX Runtime, dataset loaders or test packages are in the production environment.
- The single canonical CSS file moved unchanged from static/style.css to public/static/style.css. Existing template URLs still resolve to /static/style.css. Vercel serves it from public via its CDN; Flask is configured to serve that same URL locally. No duplicate CSS copies or frontend redesign.
- templates/ remains beside web_app.py. vercel.json explicitly includes templates/** and excludes raw data, local Chroma files, test/seed/loader/verifier scripts, docs, secrets and virtual environments from the function. Public files are served separately from the Python function.
- Three Flask error handlers now log only fixed messages, so exception details cannot expose credentials. Readable browser error responses remain intact. Credential reads are still only QDRANT_URL and QDRANT_API_KEY; no setup file was sourced during this task.
- No vector-search, scoring, runtime-add or backend-selection behavior changed. app.py, analysis.py, vector_store.py, cli.py, load_yc.py and seed_qdrant.py are byte-identical to Git HEAD.

## Verification

1. Created a clean temporary Python 3.13 environment and installed just the two production requirements and their normal transitive dependencies.
2. All 11 offline backend/deployment tests passed there. Explicitly confirmed chromadb, onnxruntime, fastembed, tokenizers, datasets, pandas and pytest are not installed.
3. Cloud startup test blocks imports of local database/embedding/seed/loader modules and blocks network connections. The Flask instance, landing page and CSS still load. A fake Qdrant query renders a full results report without local fallback or seeding. No real Qdrant requests or writes occurred.
4. Captured logs for simulated errors in analyze/add/confirmation. Neither private sentinel exception text nor tracebacks appeared in logs or browser responses.
5. Local/HW6 verification ran a live Flask server against a temporary copy of the project/database with both Qdrant variables removed. Cowlar and the existing reef user search worked; CSS and templates rendered; the CLI still retrieved Cowlar. The exact web_app.py __main__ startup call remains host 127.0.0.1, port 5001, debug=False. HTTP verification used port 5058 because an existing process already occupies 5001; that process was left alone.
6. All original chroma_store file hashes remained unchanged. No original local or remote record was inserted, deleted or updated. Local CSS bytes and full HW6 requirements are unchanged.
7. The user prompt was appended verbatim to prompt_log.md. README and portfolio were not changed.

## Remaining configuration

Set BOTH QDRANT_URL and QDRANT_API_KEY in the appropriate Vercel environment before the first build. The intentionally preserved local fallback selects Chroma if either is absent; that dependency is deliberately absent in production. Do not set the Vercel Install Command to install the full local requirements.txt.

The configuration is ready for the first Vercel build, but no Vercel build/deployment was executed, so actual hosted behavior and Linux bundle size remain unverified. No Vercel CLI was installed or invoked. The seed script remains a manual local command, never a startup/build hook.

Official references:
- https://vercel.com/docs/frameworks/backend/flask
- https://vercel.com/docs/functions/runtimes/python
- https://github.com/vercel/vercel/blob/main/packages/python-analysis/src/manifest/package.ts

Nothing was deployed, committed or pushed.
