"""Deployment configuration and runtime safety checks; no cloud calls or seeding."""

import json
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from qdrant_client import models

from web_app import app
import vector_store as store

ROOT = Path(__file__).resolve().parents[1]


class DeploymentTests(unittest.TestCase):
    def test_entrypoint_and_manifests(self):
        manifest = tomllib.loads((ROOT / 'pyproject.toml').read_text())
        self.assertEqual(manifest['tool']['vercel']['entrypoint'], 'web_app:app')
        self.assertEqual(manifest['project']['dependencies'], ['Flask==3.1.3', 'qdrant-client==1.20.0'])
        self.assertFalse(manifest['tool']['uv']['package'])
        self.assertIn('chromadb', (ROOT / 'requirements.txt').read_text())
        config = json.loads((ROOT / 'vercel.json').read_text())['functions']['web_app.py']
        self.assertEqual(config['includeFiles'], 'templates/**')
        for path in ['chroma_store/**', 'data/**', 'tests/**', 'seed_qdrant.py', 'load_yc.py']:
            self.assertIn(path, config['excludeFiles'])

    def test_static_and_templates(self):
        client = app.test_client()
        home = client.get('/')
        self.assertEqual(home.status_code, 200)
        self.assertIn(b'/static/style.css', home.data)
        css = client.get('/static/style.css')
        self.assertEqual(css.status_code, 200)
        self.assertEqual(css.data, (ROOT / 'public/static/style.css').read_bytes())
        self.assertEqual(client.get('/add-idea').status_code, 200)

    def test_cloud_startup_blocks_local_imports_and_network(self):
        code = '''
import builtins, os, socket
os.environ['QDRANT_URL'] = 'https://example.invalid'
os.environ['QDRANT_API_KEY'] = 'dummy'
original = builtins.__import__
blocked = {'chromadb', 'onnxruntime', 'fastembed', 'seed_qdrant', 'load_yc', 'datasets', 'pandas', 'tokenizers'}
def guard(name, *args, **kwargs):
    if name.split('.')[0] in blocked:
        raise AssertionError('Unexpected production import: ' + name)
    return original(name, *args, **kwargs)
builtins.__import__ = guard
def no_network(*args, **kwargs):
    raise AssertionError('Startup attempted network I/O')
socket.socket.connect = no_network
from flask import Flask
from web_app import app
from vector_store import backend_name
assert isinstance(app, Flask)
assert backend_name() == 'qdrant'
assert app.test_client().get('/').status_code == 200
assert app.test_client().get('/static/style.css').status_code == 200
'''
        result = subprocess.run([sys.executable, '-c', code], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cloud_query_does_not_access_chroma(self):
        payload = {'id': 'yc:12', 'document': 'An example company description.',
                   'metadata': {'source': 'yc', 'company_id': '12', 'company_name': 'Example'}, 'source': 'yc'}
        point = models.ScoredPoint(id=store.point_id('yc:12'), version=0, score=.8, payload=payload)
        cloud = MagicMock()
        cloud.get_collection.return_value = SimpleNamespace(config=SimpleNamespace(params=SimpleNamespace(
            vectors=models.VectorParams(size=384, distance=models.Distance.COSINE))))
        cloud.count.return_value = SimpleNamespace(count=1000)
        cloud.query_points.return_value = SimpleNamespace(points=[point])
        with patch.object(store, 'backend_name', return_value='qdrant'), patch.object(store, 'qdrant_client', return_value=cloud), patch.object(store, 'chroma_collection', side_effect=AssertionError('Local database accessed')):
            response = app.test_client().post('/analyze', data={'description': 'A normal idea'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cosine distance', response.data)
        self.assertIn(b'Example', response.data)
        cloud.upsert.assert_not_called()
        cloud.create_collection.assert_not_called()

    def test_error_logs_do_not_include_exception_details(self):
        cases = [
            ('web_app.analyze_idea', '/analyze', {'description': 'An idea'}),
            ('web_app.add_user_idea', '/add-idea', {'name': 'Title', 'description': 'An idea'}),
            ('web_app.get_user_record', '/ideas/user:test', None),
        ]
        for target, path, data in cases:
            with self.subTest(path=path), patch(target, side_effect=RuntimeError('SENTINEL_PRIVATE_VALUE')):
                with self.assertLogs(app.logger, level='ERROR') as captured:
                    client = app.test_client()
                    response = client.get(path) if data is None else client.post(path, data=data)
                self.assertEqual(response.status_code, 503)
                self.assertNotIn('SENTINEL_PRIVATE_VALUE', '\n'.join(captured.output))
                self.assertNotIn('Traceback', '\n'.join(captured.output))
                self.assertNotIn(b'SENTINEL_PRIVATE_VALUE', response.data)


if __name__ == '__main__':
    unittest.main()
