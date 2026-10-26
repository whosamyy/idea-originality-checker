"""Offline contract checks; these do not claim a Cloud Inference test passed."""

import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from qdrant_client import models

import vector_store as store
from analysis import analyze_idea
from seed_qdrant import seed_records


class FakeCloud:
    def __init__(self):
        self.points = {}
        self.calls = []

    def collection_exists(self, name):
        return True

    def get_collection(self, name):
        return SimpleNamespace(config=SimpleNamespace(params=SimpleNamespace(
            vectors=models.VectorParams(size=384, distance=models.Distance.COSINE))))

    def create_payload_index(self, *args, **kwargs):
        pass

    def retrieve(self, name, ids, **kwargs):
        return [SimpleNamespace(id=i, payload=self.points[i].payload) for i in ids if i in self.points]

    def upsert(self, name, points, wait):
        assert wait
        for point in points:
            assert isinstance(point.vector, models.Document)
            assert point.vector.model == store.MODEL
            self.points[str(point.id)] = point
        self.calls.append(len(points))

    def count(self, name, count_filter=None, **kwargs):
        source = count_filter.must[0].match.value if count_filter else None
        return SimpleNamespace(count=sum(source is None or p.payload['source'] == source for p in self.points.values()))

    def query_points(self, name, query, query_filter=None, **kwargs):
        assert isinstance(query, models.Document) and query.model == store.MODEL
        source = query_filter.must[0].match.value if query_filter else None
        points = [p for p in self.points.values() if source is None or p.payload['source'] == source]
        return SimpleNamespace(points=[models.ScoredPoint(id=p.id, version=0, score=.8,
            payload=p.payload) for p in points[:kwargs['limit']]])


class BackendTests(unittest.TestCase):
    def test_selection_requires_both(self):
        for values, expected in [({}, 'chroma'), ({'QDRANT_URL': 'dummy'}, 'chroma'),
                                 ({'QDRANT_API_KEY': 'dummy'}, 'chroma'),
                                 ({'QDRANT_URL': 'dummy', 'QDRANT_API_KEY': 'dummy'}, 'qdrant')]:
            with patch.dict(os.environ, values, clear=True):
                self.assertEqual(store.backend_name(), expected)

    def test_cloud_constructor(self):
        with patch.dict(os.environ, {'QDRANT_URL': 'https://example.invalid', 'QDRANT_API_KEY': 'dummy'}, clear=True):
            with patch('qdrant_client.QdrantClient') as client:
                store.qdrant_client()
                self.assertTrue(client.call_args.kwargs['cloud_inference'])

    def test_seed_idempotence_and_payload(self):
        records = [{'id': f'yc:{i}', 'document': f'Product description {i}',
                    'metadata': {'company_id': str(i), 'company_name': f'Company {i}', 'source': 'yc'},
                    'source': 'yc'} for i in range(1000)]
        client = FakeCloud()
        self.assertEqual(seed_records(client, records)['inserted'], 1000)
        self.assertEqual(seed_records(client, records)['inserted'], 0)
        self.assertEqual(client.calls, [100] * 10)
        self.assertEqual(len(client.points), 1000)
        self.assertEqual(store.point_id('yc:12'), store.point_id('yc:12'))
        self.assertNotEqual(store.point_id('yc:12'), store.point_id('user:12'))
        records[0]['document'] = 'Changed description'
        with self.assertRaises(RuntimeError):
            seed_records(client, records)

    def test_cloud_score_and_user_contract_without_chroma(self):
        client = FakeCloud()
        yc_id = 'yc:12'
        client.points[store.point_id(yc_id)] = models.PointStruct(id=store.point_id(yc_id),
            vector=models.Document(text='Description', model=store.MODEL),
            payload={'id':yc_id,'document':'Description','metadata':{'company_id':'12','company_name':'Example','source':'yc'},'source':'yc'})
        with patch.object(store, 'backend_name', return_value='qdrant'), patch.object(store, 'qdrant_client', return_value=client), patch.object(store, 'chroma_collection', side_effect=AssertionError('Chroma accessed')):
            store.add_user_record('user:test', 'Test', 'User description')
            self.assertEqual(store.get_user_record('user:test')['document'], 'User description')
            report = analyze_idea('A query')
        match = report['closest_known_analog']
        self.assertEqual(match['score'], .8)
        self.assertAlmostEqual(match['distance'], .2)
        self.assertEqual(report['backend'], 'qdrant')
        self.assertIn('native_results', report['raw_retrieval']['real_companies'])
        self.assertEqual(report['yc_record_count'], 1)

    def test_cloud_flask_labels_and_confirmation(self):
        from web_app import app
        client = FakeCloud()
        item_id = 'yc:12'
        client.points[store.point_id(item_id)] = models.PointStruct(id=store.point_id(item_id),
            vector=models.Document(text='Description', model=store.MODEL),
            payload={'id': item_id, 'document': 'Description',
                     'metadata': {'company_id': '12', 'company_name': 'Example', 'source': 'yc'}, 'source': 'yc'})
        with patch.object(store, 'backend_name', return_value='qdrant'), patch.object(store, 'qdrant_client', return_value=client), patch.object(store, 'chroma_collection', side_effect=AssertionError('Chroma accessed')):
            http = app.test_client()
            response = http.post('/analyze', data={'description': 'A query'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Cosine distance', response.data)
            self.assertIn(b'Raw Qdrant score', response.data)
            self.assertNotIn(b'<span>Chroma distance</span>', response.data)
            response = http.post('/add-idea', data={'name': 'Test', 'description': 'Description'})
            self.assertEqual(response.status_code, 303)
            self.assertEqual(http.get(response.location).status_code, 200)

    def test_remote_errors_do_not_leak(self):
        with self.assertRaisesRegex(RuntimeError, '^Qdrant request failed') as raised:
            with store.qdrant_errors():
                raise ValueError('dummy private detail')
        self.assertNotIn('private detail', str(raised.exception))


if __name__ == '__main__':
    unittest.main()
