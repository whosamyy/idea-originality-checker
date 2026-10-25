"""Small interactive interface for the existing idea-search functions."""

from chromadb.errors import ChromaError

from analysis import analyze_idea
from app import add_user_idea


def read_required(prompt):
    """Repeat a prompt until the user supplies nonblank text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('Please enter a non-empty value.')


def show_report(report):
    """Format an analysis result without changing retrieval or statistics."""
    print('\nCOMPETITIVE LANDSCAPE')
    print('Distances are shown to 6 decimal places; lower means closer.')
    analog = report['closest_known_analog']
    print('\nClosest Known Analog')
    if analog:
        print(f"{analog['company_name']} — distance {analog['distance']:.6f}")
    else:
        print('No YC companies are available.')
    print('\nTop 5 Existing YC Companies')
    for match in report['closest_existing_companies']:
        print(f"\n{match['rank']}. {match['company_name']} — distance {match['distance']:.6f}")
        print(f"   {match['short_description']}")
        for label, key in [('Industry', 'industry'), ('Subindustry', 'subindustry'),
                           ('Batch', 'batch'), ('YC URL', 'yc_url')]:
            if match.get(key):
                print(f'   {label}: {match[key]}')

    if report['user_created_matches']:
        print('\nUser-Created Ideas (separate from YC companies)')
        for match in report['user_created_matches']:
            print(f"Overall rank {match['rank']}: {match['company_name']} — distance {match['distance']:.6f}")
            print(f"   ID: {match['id']}")
            print(f"   {match['short_description']}")

    neighborhood = report['market_neighborhood']
    print(f"\nMarket Neighborhood — top {neighborhood['sample_size']} YC results")
    print(f"Distinct recorded industries: {neighborhood['distinct_industries']}")
    for label, key in [('Industries', 'industries'), ('Subindustries', 'subindustries')]:
        counts = ', '.join(f"{entry['name']} ({entry['count']})" for entry in neighborhood[key])
        print(f"{label}: {counts or 'Unavailable'}")
    if neighborhood['distinct_industries'] == 1:
        print('All available industry labels are in one industry.')
    elif neighborhood['distinct_industries'] > 1:
        print('The retrieved companies span multiple industries.')
    for label, key in [('industry', 'missing_industry_count'), ('subindustry', 'missing_subindustry_count')]:
        if neighborhood[key]:
            print(f"Missing {label} labels: {neighborhood[key]}")

    print('\nSimilarity Pattern — YC results')
    pattern = report['similarity_pattern']
    for label, key in [('Nearest distance', 'nearest_distance'),
                       ('Average distance of top 5', 'average_distance_top_5'),
                       ('Average distance of top 10', 'average_distance_top_10'),
                       ('Gap between rank 1 and rank 5', 'gap_rank_1_to_rank_5')]:
        value = pattern[key]
        print(f"{label}: {value:.6f}" if value is not None else f'{label}: Unavailable')
    print('\nConclusion')
    print(report['conclusion'])


def main():
    while True:
        print('\nHOW ORIGINAL IS MY IDEA?')
        print('1. Analyze a startup idea')
        print('2. Add a startup idea to the database')
        print('3. Quit')
        choice = input('Choose an option: ').strip()
        if choice == '3':
            print('Goodbye!')
            return
        if choice not in ('1', '2'):
            print('Please choose 1, 2, or 3.')
            continue
        try:
            if choice == '1':
                description = read_required('Describe your startup/product idea: ')
                show_report(analyze_idea(description))
            else:
                name = read_required('Idea/startup name: ')
                description = read_required('Describe what it does: ')
                idea_id = add_user_idea(name, description)
                print(f'Idea added. Generated ID: {idea_id}')
                while True:
                    answer = input('Analyze this idea now? [y/N]: ').strip().lower()
                    if answer in ('y', 'yes', 'n', 'no', ''):
                        break
                    print('Please answer y or n.')
                if answer in ('y', 'yes'):
                    show_report(analyze_idea(description))
        except (ChromaError, ValueError, OSError, RuntimeError) as error:
            print(f'Could not complete that operation: {error}')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\nGoodbye!')
