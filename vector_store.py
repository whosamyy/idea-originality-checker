"""Small backend boundary: local Chroma by default, optional Qdrant Cloud."""

import os
from contextlib import contextmanager
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

CHROMA_PATH = Path(__file__).resolve().parent / 'chroma_store'
COLLECTION = 'yc_startups'
MODEL = 'sentence-transformers/all-minilm-l6-v2'
VECTOR_SIZE = 384


def backend_name():
    return 'qdrant' if os.environ.get('QDRANT_URL') and os.environ.get('QDRANT_API_KEY') else 'chroma'


@contextmanager
def qdrant_errors():
    # Do not expose credentials, request headers, URLs or remote error bodies.
    try:
        yield
    except Exception:
        raise RuntimeError('Qdrant request failed. Check the connection, collection and Cloud Inference settings.') from None


def qdrant_client():
    if backend_name() != 'qdrant':
        raise RuntimeError('Set both QDRANT_URL and QDRANT_API_KEY to use Qdrant.')
    from qdrant_client import QdrantClient
    with qdrant_errors():
        return QdrantClient(url=os.environ['QDRANT_URL'], api_key=os.environ['QDRANT_API_KEY'],
                            cloud_inference=True, timeout=90)


def point_id(item_id):
    # Qdrant requires integer/UUID point IDs. Keep the original yc:/user: ID in payload.
    return str(uuid5(NAMESPACE_URL, 'idea-originality-checker:' + item_id))


def source_filter(source):
    from qdrant_client import models
    return models.Filter(must=[models.FieldCondition(key='source', match=models.MatchValue(value=source))])


def validate_qdrant_collection(client):
    from qdrant_client import models
    with qdrant_errors():
        vectors = client.get_collection(COLLECTION).config.params.vectors
    if not isinstance(vectors, models.VectorParams) or vectors.size != VECTOR_SIZE or vectors.distance != models.Distance.COSINE:
        raise RuntimeError('Expected an unnamed 384-dimensional cosine collection; existing collection was not changed.')


def chroma_collection():
    import chromadb
    return chromadb.PersistentClient(path=str(CHROMA_PATH)).get_collection(COLLECTION)


def add_user_record(item_id, name, description):
    metadata = {'company_name': name, 'source': 'user'}
    if backend_name() == 'chroma':
        chroma_collection().add(ids=[item_id], documents=[description], metadatas=[metadata])
        return
    from qdrant_client import models
    client = qdrant_client()
    validate_qdrant_collection(client)
    with qdrant_errors():
        client.upsert(COLLECTION, points=[models.PointStruct(
            id=point_id(item_id), vector=models.Document(text=description, model=MODEL),
            payload={'id': item_id, 'document': description, 'metadata': metadata, 'source': 'user'},
        )], wait=True)


def get_user_record(item_id):
    if not item_id.startswith('user:'):
        return None
    if backend_name() == 'chroma':
        result = chroma_collection().get(ids=[item_id], include=['documents', 'metadatas'])
        if not result['ids']:
            return None
        document, metadata = result['documents'][0], result['metadatas'][0] or {}
    else:
        client = qdrant_client()
        with qdrant_errors():
            records = client.retrieve(COLLECTION, ids=[point_id(item_id)], with_payload=True)
        if not records or (records[0].payload or {}).get('id') != item_id:
            return None
        payload = records[0].payload
        document, metadata = payload['document'], payload.get('metadata', {})
    if metadata.get('source') != 'user':
        return None
    return {'id': item_id, 'document': document, 'metadata': metadata}


def qdrant_result(points):
    """Adapt shape only; retain native scores and full native results."""
    return {
        'ids': [[p.payload['id'] for p in points]],
        'documents': [[p.payload['document'] for p in points]],
        'metadatas': [[p.payload['metadata'] for p in points]],
        'distances': [[1.0 - p.score for p in points]],
        'scores': [[p.score for p in points]],
        'native_results': [p.model_dump(mode='json') for p in points],
    }


def retrieve_idea(description, limit=10):
    if backend_name() == 'qdrant':
        from qdrant_client import models
        client = qdrant_client()
        validate_qdrant_collection(client)
        with qdrant_errors():
            total = client.count(COLLECTION, exact=True).count
            yc_count = client.count(COLLECTION, count_filter=source_filter('yc'), exact=True).count
            query = models.Document(text=description, model=MODEL)
            raw_all = client.query_points(COLLECTION, query=query, limit=limit, with_payload=True).points
            raw_real = client.query_points(COLLECTION, query=query, query_filter=source_filter('yc'),
                                           limit=limit, with_payload=True).points
        return {
            'backend': 'qdrant', 'collection_count': total, 'yc_record_count': yc_count,
            'raw_all': qdrant_result(raw_all), 'raw_real': qdrant_result(raw_real),
            'scoring': {'distance_label': 'Cosine distance', 'metric': 'cosine',
                        'native_score_label': 'Qdrant cosine similarity', 'higher_score_is_closer': True,
                        'note': 'Cosine distance = 1 − raw Qdrant cosine score. Lower distance is closer; higher raw score is closer. These are not Chroma distances.'},
        }
    collection = chroma_collection()
    records = collection.get(include=['metadatas'])
    real_ids = [item_id for item_id, metadata in zip(records['ids'], records['metadatas'])
                if item_id.startswith('yc:') and (metadata or {}).get('company_id')
                and (metadata or {}).get('source') != 'user']
    empty = {'ids': [[]], 'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
    total = collection.count()
    raw_all = collection.query(query_texts=[description], n_results=min(limit, total),
                               include=['documents', 'metadatas', 'distances']) if total else empty
    raw_real = collection.query(query_texts=[description], ids=real_ids, n_results=min(limit, len(real_ids)),
                                include=['documents', 'metadatas', 'distances']) if real_ids else empty
    return {
        'backend': 'chroma', 'collection_count': total, 'yc_record_count': len(real_ids),
        'raw_all': raw_all, 'raw_real': raw_real,
        'scoring': {'distance_label': 'Chroma distance', 'metric': 'squared_l2',
                    'native_score_label': None, 'higher_score_is_closer': False,
                    'note': 'Raw Chroma squared L2 distances, not an originality score. Lower is closer. Their meaning depends on the query and corpus.'},
    }
