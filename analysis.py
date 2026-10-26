"""Reusable local retrieval analysis; no interface or LLM calls."""

from collections import Counter
from statistics import mean

from vector_store import retrieve_idea

TOP_RESULTS = 10
DISPLAY_COMPANIES = 5
SHORT_DESCRIPTION_CHARS = 240


def clean_matches(raw):
    """Keep distances, full documents and metadata alongside display fields."""
    matches = []
    for rank, (item_id, document, metadata, distance) in enumerate(zip(
        raw['ids'][0], raw['documents'][0], raw['metadatas'][0], raw['distances'][0]
    ), 1):
        metadata = metadata or {}
        document = document or ''
        if metadata.get('source') == 'user':
            source = 'user'
        elif item_id.startswith('yc:') and metadata.get('company_id'):
            source = 'yc'
        else:
            source = 'unknown'
        short = ' '.join(document.split())
        if len(short) > SHORT_DESCRIPTION_CHARS:
            short = short[:SHORT_DESCRIPTION_CHARS].rsplit(' ', 1)[0] + '…'
        matches.append({
            'id': item_id, 'source': source, 'rank': rank,
            'company_name': metadata.get('company_name', item_id),
            'short_description': short, 'document': document,
            'industry': metadata.get('industry'),
            'subindustry': metadata.get('subindustry'),
            'batch': metadata.get('batch'), 'yc_url': metadata.get('yc_url'),
            'metadata': metadata, 'distance': distance,
        })
    if 'scores' in raw:
        for match, score in zip(matches, raw['scores'][0]):
            match['score'] = score
            match['score_metric'] = 'cosine_similarity'
    return matches


def summarize_matches(matches):
    """Describe the retrieved YC neighborhood without relevance thresholds."""
    def frequencies(field):
        counts = Counter(m[field] for m in matches if m.get(field))
        return [{'name': name, 'count': count}
                for name, count in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))]

    industries = frequencies('industry')
    subindustries = frequencies('subindustry')
    distinct = len(industries)
    neighborhood = {
        'sample_size': len(matches),
        'industries': industries, 'subindustries': subindustries,
        'distinct_industries': distinct,
        'distinct_subindustries': len(subindustries),
        'missing_industry_count': sum(not m.get('industry') for m in matches),
        'missing_subindustry_count': sum(not m.get('subindustry') for m in matches),
        'distribution': ('unknown' if not distinct else
                         'single_recorded_industry' if distinct == 1 else
                         'multiple_recorded_industries'),
        'largest_industry_count': industries[0]['count'] if industries else 0,
    }
    distances = [m['distance'] for m in matches]
    pattern = {
        'sample_size': len(distances),
        'top_5_sample_size': min(DISPLAY_COMPANIES, len(distances)),
        'nearest_distance': distances[0] if distances else None,
        'average_distance_top_5': mean(distances[:DISPLAY_COMPANIES]) if distances else None,
        'average_distance_top_10': mean(distances) if distances else None,
        'gap_rank_1_to_rank_5': (distances[4] - distances[0]) if len(distances) >= 5 else None,
    }
    if not matches:
        conclusion = 'No real YC company matches are available in the current collection.'
    else:
        conclusion = (
            f"The nearest retrieved YC result is {matches[0]['company_name']} "
            f"(distance {distances[0]:.6f}). "
            f"The {len(matches)} retrieved YC records span {distinct} recorded industries"
        )
        if industries:
            leaders = ', '.join(i['name'] for i in industries if i['count'] == industries[0]['count'])
            conclusion += f"; the most frequent: {leaders} ({industries[0]['count']} records each). "
        else:
            conclusion += '; industry metadata is unavailable. '
        conclusion += (
            'These are nearest semantic neighbors, not verified competitors; '
            'this limited corpus cannot establish originality.'
        )
    return neighborhood, pattern, conclusion


def analyze_idea(description: str) -> dict:
    """Return raw retrieval, YC matches, user matches and deterministic analysis.

    Ranks in real_company_matches are among YC companies. Ranks in all_matches
    and user_created_matches are among the overall top 10, including user ideas.
    Existing YC records have no source field, so their namespace and company_id
    identify them without modifying the database.
    """
    if not isinstance(description, str) or not description.strip():
        raise ValueError('description must be a nonempty string')
    description = description.strip()
    retrieval = retrieve_idea(description, TOP_RESULTS)
    raw_all, raw_real = retrieval['raw_all'], retrieval['raw_real']
    all_matches = clean_matches(raw_all)
    real_matches = clean_matches(raw_real)
    neighborhood, pattern, conclusion = summarize_matches(real_matches)
    return {
        'query': description, 'collection': 'yc_startups',
        'collection_count': retrieval['collection_count'], 'yc_record_count': retrieval['yc_record_count'],
        'backend': retrieval['backend'], 'scoring': retrieval['scoring'],
        'raw_retrieval': {'all_items': raw_all, 'real_companies': raw_real},
        'all_matches': all_matches,
        'user_created_matches': [m for m in all_matches if m['source'] == 'user'],
        'real_company_matches': real_matches,
        'closest_existing_companies': real_matches[:DISPLAY_COMPANIES],
        'closest_known_analog': real_matches[0] if real_matches else None,
        'market_neighborhood': neighborhood, 'similarity_pattern': pattern,
        'conclusion': conclusion,
    }
