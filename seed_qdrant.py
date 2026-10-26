"""Manually seed exactly the existing 1,000 YC records; never seed on Flask startup."""

import shutil
import tempfile
from pathlib import Path

from vector_store import (CHROMA_PATH, COLLECTION, MODEL, VECTOR_SIZE, point_id,
                          qdrant_client, qdrant_errors, source_filter,
                          validate_qdrant_collection)

BATCH_SIZE = 100


def read_yc_snapshot():
    # Chroma can write internal state on open, even for get(). Work on a copy.
    # No embedding model is run: get() reads stored documents/metadata only.
    import chromadb
    with tempfile.TemporaryDirectory(prefix='yc-seed-snapshot-') as folder:
        copy = Path(folder) / 'chroma_store'
        shutil.copytree(CHROMA_PATH, copy)
        collection = chromadb.PersistentClient(path=str(copy)).get_collection(COLLECTION)
        saved = collection.get(include=['documents', 'metadatas'])
        records = []
        for item_id, document, metadata in zip(saved['ids'], saved['documents'], saved['metadatas']):
            metadata = metadata or {}
            if item_id.startswith('yc:') and metadata.get('company_id') and metadata.get('source') != 'user':
                records.append({'id': item_id, 'document': document,
                                'metadata': {**metadata, 'source': 'yc'}, 'source': 'yc'})
        if len(records) != 1000 or len({r['id'] for r in records}) != 1000:
            raise RuntimeError('Expected exactly 1,000 distinct YC records; nothing was uploaded.')
        return sorted(records, key=lambda row: row['id'])


def seed_records(client, records):
    from qdrant_client import models
    with qdrant_errors():
        exists = client.collection_exists(COLLECTION)
    if not exists:
        with qdrant_errors():
            client.create_collection(COLLECTION, vectors_config=models.VectorParams(
                size=VECTOR_SIZE, distance=models.Distance.COSINE))
    validate_qdrant_collection(client)
    with qdrant_errors():
        # Qdrant Cloud strict filtering requires an indexed source field.
        client.create_payload_index(COLLECTION, field_name='source',
                                    field_schema=models.PayloadSchemaType.KEYWORD, wait=True)
    inserted = 0
    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start:start + BATCH_SIZE]
        with qdrant_errors():
            existing = client.retrieve(COLLECTION, ids=[point_id(r['id']) for r in batch], with_payload=True)
        by_id = {str(point.id): point.payload for point in existing}
        pending = []
        for record in batch:
            stored = by_id.get(point_id(record['id']))
            if stored is not None:
                if any(stored.get(key) != value for key, value in record.items()):
                    raise RuntimeError('A stored point differs from the seed snapshot; no overwrite was attempted.')
                continue
            pending.append(models.PointStruct(id=point_id(record['id']),
                vector=models.Document(text=record['document'], model=MODEL), payload=record))
        if pending:
            with qdrant_errors():
                client.upsert(COLLECTION, points=pending, wait=True)
            inserted += len(pending)
        print(f'Checked {min(start + BATCH_SIZE, len(records))} / {len(records)}; added {inserted}', flush=True)
    with qdrant_errors():
        yc_count = client.count(COLLECTION, count_filter=source_filter('yc'), exact=True).count
        total = client.count(COLLECTION, exact=True).count
    if yc_count != 1000:
        raise RuntimeError('Remote YC count is not exactly 1,000; existing remote records were not deleted.')
    print(f'YC count: {yc_count}; total collection count: {total}; added this run: {inserted}', flush=True)
    return {'yc_count': yc_count, 'total_count': total, 'inserted': inserted}


def main():
    client = qdrant_client()  # Requires both environment variables; never falls back for seeding.
    with qdrant_errors():
        client.get_collections()
    print('Qdrant connection verified. Reading a temporary local snapshot.', flush=True)
    seed_records(client, read_yc_snapshot())


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as error:
        raise SystemExit(str(error)) from None
