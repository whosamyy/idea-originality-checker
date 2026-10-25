"""Run local analysis checks and save actual reports; inserts no records."""

import hashlib
import json
from pathlib import Path
from statistics import mean

import chromadb

from analysis import analyze_idea, clean_matches, summarize_matches

ROOT = Path(__file__).resolve().parent
QUERIES = {
    'A — cattle monitoring': 'A device worn by cattle that warns ranchers when an animal may be ill or ready to breed.',
    'B — remote connectivity': 'Let small wireless gadgets send updates from remote areas where phones have no signal, through equipment orbiting Earth.',
    'C — meeting follow-up': 'Software that listens to meetings and automatically turns conversations into organized follow-up tasks.',
    'D — scattered work documents': 'A single place to find documents scattered across all the online services my team uses.',
    'Nonsense': 'Quantum marshmallow nebula dances inside a purple theorem.',
    'User-item separation': 'Help ocean ecologists spot stressed or unhealthy stony sea organisms being regrown, using submerged imaging and automatic warnings.',
}


def fingerprint(collection):
    records = collection.get(include=['documents', 'metadatas', 'embeddings'])
    rows = sorted(zip(records['ids'], records['documents'], records['metadatas'], records['embeddings'].tolist()))
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()


def main():
    # Exact arithmetic, incomplete metadata and empty-neighborhood behavior.
    raw = {'ids': [['yc:1', 'user:abc']], 'documents': [['A company', 'A user idea']],
           'metadatas': [[{'company_id': '1', 'company_name': 'Example'}, {'source': 'user'}]],
           'distances': [[0.2, 0.4]]}
    cleaned = clean_matches(raw)
    assert [m['source'] for m in cleaned] == ['yc', 'user']
    assert cleaned[0]['metadata'] == raw['metadatas'][0][0]
    fixture = [dict(distance=d, industry='B2B' if i < 3 else None,
                    subindustry='Tools' if i < 2 else None, company_name='Example')
               for i, d in enumerate([0.2, 0.4, 0.8, 1.2, 1.7])]
    neighborhood, stats, _ = summarize_matches(fixture)
    assert stats['average_distance_top_5'] == mean([0.2, 0.4, 0.8, 1.2, 1.7])
    assert stats['gap_rank_1_to_rank_5'] == 1.7 - 0.2
    assert neighborhood['missing_industry_count'] == 2
    assert neighborhood['industries'] == [{'name': 'B2B', 'count': 3}]
    assert summarize_matches([])[1]['nearest_distance'] is None
    assert summarize_matches(fixture[:2])[1]['gap_rank_1_to_rank_5'] is None
    for value in ['', '   ', None]:
        try:
            analyze_idea(value)
        except ValueError:
            pass
        else:
            raise AssertionError('Blank/invalid input must fail before database access')

    client = chromadb.PersistentClient(path=str(ROOT / 'chroma_store'))
    collection = client.get_collection('yc_startups')
    smoke = client.get_collection('startup_ideas')
    before = (fingerprint(collection), fingerprint(smoke))
    reports = {}
    for label, query in QUERIES.items():
        report = analyze_idea(query)
        assert len(report['real_company_matches']) == 10
        assert len(report['closest_existing_companies']) == 5
        assert all(m['source'] == 'yc' for m in report['real_company_matches'])
        distances = report['raw_retrieval']['real_companies']['distances'][0]
        assert [m['distance'] for m in report['real_company_matches']] == distances
        assert report['similarity_pattern']['average_distance_top_10'] == mean(distances)
        assert report['closest_known_analog'] == report['real_company_matches'][0]
        assert report['collection_count'] == 1001 and report['yc_record_count'] == 1000
        assert report == analyze_idea(query), 'Repeated report must be deterministic'
        reports[label] = report
        print('\n'+label)
        for m in report['closest_existing_companies']:
            print(m['rank'], m['company_name'], m['distance'])
        print(json.dumps(report['market_neighborhood']))
        print(json.dumps(report['similarity_pattern']))
        print(report['conclusion'])
    user_report = reports['User-item separation']
    assert user_report['all_matches'][0]['source'] == 'user'
    assert user_report['user_created_matches'][0]['rank'] == 1
    assert len(user_report['real_company_matches']) == 10
    after = (fingerprint(collection), fingerprint(smoke))
    assert before == after, 'Analysis must not mutate records, metadata or embeddings'
    assert collection.count() == 1001 and smoke.count() == 10
    (ROOT / 'data' / 'analysis_results.json').write_text(json.dumps(reports, indent=2)+'\n')
    print('\nAll checks passed. All records, metadata and embedding vectors unchanged.')


if __name__ == '__main__':
    main()
