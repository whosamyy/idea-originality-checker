"""Manual cloud integration test. Adds one labeled REMOTE user idea per run.

Requires QDRANT_URL and QDRANT_API_KEY in the same shell. Never prints them.
No local Chroma database is opened by this verification script.
"""

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, unquote
from urllib.request import Request, urlopen

from vector_store import COLLECTION, backend_name, qdrant_client, qdrant_errors, source_filter

ROOT = Path(__file__).resolve().parent
BASE = 'http://127.0.0.1:5059'
QUERIES = {
    'Cowlar': 'A device worn by cattle that warns ranchers when an animal may be ill or ready to breed.',
    'Hubble Network': 'Let small wireless gadgets send updates from remote areas where phones have no signal, through equipment orbiting Earth.',
    'Meeting follow-up': 'Software that listens to meetings and automatically turns conversations into organized follow-up tasks.',
}


def store_hashes():
    folder = ROOT / 'chroma_store'
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file()}


def request(path, fields=None):
    data = urlencode(fields).encode() if fields is not None else None
    with urlopen(Request(BASE + path, data=data), timeout=180) as response:
        return response.read().decode(), response.url


def start_flask():
    process = subprocess.Popen([sys.executable, '-c',
        "from web_app import app; app.run(host='127.0.0.1', port=5059, debug=False)"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(100):
        if process.poll() is not None:
            raise RuntimeError('Test Flask server could not start on port 5059.')
        try:
            request('/')
            return process
        except (URLError, ConnectionError):
            time.sleep(.1)
    process.terminate()
    process.wait(timeout=10)
    raise RuntimeError('Test Flask server did not become ready.')


def stop_flask(process):
    process.terminate()
    process.wait(timeout=10)


def main():
    if backend_name() != 'qdrant':
        raise RuntimeError('Set both QDRANT_URL and QDRANT_API_KEY in this shell before running this test.')
    client = qdrant_client()
    with qdrant_errors():
        client.get_collections()
    print('Cloud connection confirmed.', flush=True)
    before = store_hashes()
    for _ in range(2):
        # Capture, rather than dump, unexpected process output that could expose a credential.
        result = subprocess.run([sys.executable, 'seed_qdrant.py'], cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError('Seeding failed. Check Cloud Inference and collection configuration.')
        print(result.stdout, end='')  # Seeder emits counts and fixed messages only.
    with qdrant_errors():
        yc_count = client.count(COLLECTION, count_filter=source_filter('yc'), exact=True).count
        before_total = client.count(COLLECTION, exact=True).count
    assert yc_count == 1000
    from analysis import analyze_idea
    observed = {}
    process = start_flask()
    try:
        for label, query in QUERIES.items():
            html, _ = request('/analyze', {'description': query})
            assert 'Your startup' in html and 'Cosine distance' in html and 'Raw Qdrant score' in html
            report = analyze_idea(query)
            observed[label] = {'target_rank': next((m['rank'] for m in report['real_company_matches']
                if m['company_name'] == ('Onward' if label == 'Meeting follow-up' else label)), None), 'top_10': report['real_company_matches']}
        name = 'Development test — Cloud Beehive Sound Monitor'
        description = 'An acoustic sensor listens inside honeybee hives to warn beekeepers of queen loss, swarming, or disease before visible colony damage.'
        html, url = request('/add-idea', {'name': name, 'description': description})
        idea_id = unquote(url.rsplit('/', 1)[-1])
        assert idea_id.startswith('user:') and name in html
        html, _ = request('/analyze', {'description': description})
        assert name in html and 'Nearby user-created ideas' in html
        immediate = analyze_idea(description)
        immediate_match = next(m for m in immediate['user_created_matches'] if m['id'] == idea_id)
    finally:
        stop_flask(process)
    # First Flask process has fully exited before the second starts.
    process = start_flask()
    try:
        html, _ = request('/ideas/' + idea_id)
        assert idea_id in html and name in html
        html, _ = request('/analyze', {'description': description})
        assert name in html
        restarted = analyze_idea(description)
        restart_match = next(m for m in restarted['user_created_matches'] if m['id'] == idea_id)
    finally:
        stop_flask(process)
    with qdrant_errors():
        total = client.count(COLLECTION, exact=True).count
        final_yc = client.count(COLLECTION, count_filter=source_filter('yc'), exact=True).count
    assert total == before_total + 1 and final_yc == 1000
    assert before == store_hashes(), 'Original Chroma files changed.'
    report = {'yc_count': final_yc, 'total_count': total, 'queries': observed,
              'user_id': idea_id, 'immediate_match': immediate_match, 'restart_match': restart_match,
              'original_chroma_files_unchanged': True}
    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data/qdrant_cloud_verification.json').write_text(json.dumps(report, indent=2))
    print(f'Cloud verified: {final_yc} YC records, {total} total. User idea ranks: '
          f"{immediate_match['rank']} immediately, {restart_match['rank']} after restart.")
    for label, result in observed.items():
        print(f"{label}: target rank {result['target_rank']}; nearest {result['top_10'][0]['company_name']}")


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, AssertionError, HTTPError):
        raise SystemExit('Cloud verification incomplete. Check that both environment variables are available, Cloud Inference is enabled, and the collection uses unnamed 384-dimensional cosine vectors. No deployment was attempted.') from None
