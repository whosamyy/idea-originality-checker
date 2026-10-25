"""Load exactly 1,000 real YC companies and inspect raw semantic-search results."""

import csv
import json
import random
import time
from pathlib import Path
from urllib.parse import urljoin

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from tokenizers import Tokenizer


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data' / 'yc-companies.csv'
LIMIT = 1000
BATCH_SIZE = 100
MIN_DESCRIPTION_CHARS = 40
MIN_DESCRIPTION_WORDS = 8
METADATA_FIELDS = {
    'company_name': 'Company Name', 'company_id': 'Company ID',
    'industry': 'Industry', 'subindustry': 'Subindustry', 'batch': 'Batch',
    'status': 'Status', 'yc_url': 'YC DC Company URL',
}
SEARCHES = [
    ('Query A — focus/productivity', 'A tool that notices when college students drift to social media during homework and rewards them for staying focused.'),
    ('Query B — food waste/recipes', "People describe what's sitting in their fridge and get dinner suggestions before their groceries go bad."),
    ('Query C — meeting follow-up', 'Software that listens to meetings and automatically turns conversations into organized follow-up tasks.'),
    ('Query D — earned pay access', 'A service that lets employees withdraw money they have already earned instead of waiting until the end of the month.'),
    ('Nonsense', 'Quantum marshmallow nebula dances inside a purple theorem.'),
]


def main():
    total_started = time.perf_counter()
    with SOURCE.open(newline='', encoding='utf-8-sig') as source:
        reader = csv.DictReader(source)
        required = {'One Liner', 'Long Description', 'Tags', *METADATA_FIELDS.values()}
        missing_fields = required - set(reader.fieldnames or [])
        if missing_fields:
            raise ValueError(f'Missing dataset fields: {sorted(missing_fields)}')
        rows = list(reader)
    # Fixed order, independent of query results; avoids the CSV's alphabetical bias.
    random.Random(42).shuffle(rows)
    selected, seen, skipped = [], set(), {}
    inspected = 0
    for row in rows:
        inspected += 1
        company_id = row['Company ID'].strip()
        descriptive = ' '.join(row[k].strip() for k in ('One Liner', 'Long Description'))
        reason = None
        if not company_id:
            reason = 'missing_company_id'
        elif company_id in seen:
            reason = 'duplicate_company_id'
        elif len(descriptive.strip()) < MIN_DESCRIPTION_CHARS or len(descriptive.split()) < MIN_DESCRIPTION_WORDS:
            reason = 'insufficient_description'
        if reason:
            skipped[reason] = skipped.get(reason, 0) + 1
            continue
        seen.add(company_id)
        # Name is metadata only. Put tags before long text so they survive truncation.
        document = '\n'.join(
            f'{label}: {row[field].strip()}'
            for label, field in [('Summary', 'One Liner'), ('Tags', 'Tags'), ('Description', 'Long Description')]
            if row[field].strip()
        )
        metadata = {key: row[field].strip() for key, field in METADATA_FIELDS.items() if row[field].strip()}
        if 'yc_url' in metadata:
            metadata['yc_url'] = urljoin('https://www.ycombinator.com', metadata['yc_url'])
        selected.append({'id': f'yc:{company_id}', 'document': document, 'metadata': metadata})
        if len(selected) == LIMIT:
            break
    if len(selected) != LIMIT:
        raise ValueError(f'Only {len(selected)} usable records; expected {LIMIT}')

    print(f'Inspected {inspected}; skipped {sum(skipped.values())}; selected {len(selected)}.', flush=True)
    started = time.perf_counter()
    embedding = DefaultEmbeddingFunction()
    # Mirror the installed default model's 256-token limit explicitly. Store the
    # actual text embedded, rather than silently displaying a longer document.
    tokenizer = Tokenizer.from_file(str(Path.home() / '.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx/tokenizer.json'))
    tokenizer.no_padding()
    tokenizer.no_truncation()
    truncated = 0
    for item in selected:
        tokens = tokenizer.encode(item['document'])
        if len(tokens.ids) > 256:
            item['document'] = item['document'][:tokens.offsets[254][1]]
            truncated += 1
        assert len(tokenizer.encode(item['document']).ids) <= 256

    client = chromadb.PersistentClient(path=str(ROOT / 'chroma_store'))
    # Collection is deliberately separate from startup_ideas.
    collection = client.get_or_create_collection('yc_startups', embedding_function=embedding)
    before = collection.count()
    prior = collection.get(include=['documents', 'metadatas'])
    existing = set(prior['ids'])
    expected = {item['id']: item for item in selected}
    if not existing <= set(expected):
        raise ValueError('Existing collection contains IDs outside the deterministic selection.')
    for company_id, document, metadata in zip(prior['ids'], prior['documents'], prior['metadatas']):
        if document != expected[company_id]['document'] or metadata != expected[company_id]['metadata']:
            raise ValueError(f'Existing content differs for {company_id}; stopping without changing it.')
    pending = [item for item in selected if item['id'] not in existing]
    print(f'Collection initially {before}; embedding/inserting {len(pending)} records in batches of {BATCH_SIZE}...', flush=True)
    batch_started = time.perf_counter()
    for offset in range(0, len(pending), BATCH_SIZE):
        batch = pending[offset:offset + BATCH_SIZE]
        collection.add(
            ids=[item['id'] for item in batch],
            documents=[item['document'] for item in batch],
            metadatas=[item['metadata'] for item in batch],
        )
        print(f'Loaded {collection.count()} / {LIMIT}', flush=True)
    batch_seconds = time.perf_counter() - batch_started
    loading_seconds = time.perf_counter() - started
    saved = collection.get(include=['documents'])
    assert collection.count() == LIMIT, 'This stage must contain exactly 1,000 real records.'
    assert set(saved['ids']) == {item['id'] for item in selected}
    smoke_count = client.get_collection('startup_ideas').count()
    assert smoke_count == 10, 'The original smoke-test collection must remain intact.'
    report = {
        'chromadb_version': chromadb.__version__, 'source': str(SOURCE),
        'selection': 'fixed shuffle seed 42, first 1000 usable; independent of queries',
        'rows_inspected': inspected, 'skipped': skipped, 'selected': len(selected),
        'descriptions_truncated_to_256_tokens': truncated,
        'count_before': before, 'inserted': len(pending), 'count_after': collection.count(),
        'unique_ids': len(set(saved['ids'])), 'unique_documents': len(set(saved['documents'])),
        'smoke_collection_count': smoke_count,
        'embedding_and_insertion_seconds': batch_seconds,
        'total_loading_seconds': loading_seconds,
        'total_seconds_including_selection': time.perf_counter() - total_started,
        'seconds_per_inserted_item': batch_seconds / len(pending) if pending else None,
        'queries': [],
    }
    for label, query in SEARCHES:
        print(f'Searching: {label}', flush=True)
        result = collection.query(query_texts=[query], n_results=10, include=['documents', 'metadatas', 'distances'])
        matches = [dict(id=i, document=d, metadata=m, distance=distance)
                   for i, d, m, distance in zip(result['ids'][0], result['documents'][0], result['metadatas'][0], result['distances'][0])]
        report['queries'].append({'label': label, 'query': query, 'matches': matches})
    (ROOT / 'data' / '1000_last_run.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
