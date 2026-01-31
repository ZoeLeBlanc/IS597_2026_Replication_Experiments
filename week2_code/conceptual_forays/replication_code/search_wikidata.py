"""
Search Wikidata - Python replication of 4search_wikidata.R
"""
import requests
import pandas as pd
import os

# Set data directory
DATA_DIR = "../data"


def query_wikidata(query):
    """Query Wikidata SPARQL endpoint"""
    url = "https://query.wikidata.org/sparql"
    headers = {'Accept': 'application/json'}

    try:
        response = requests.get(url, params={'query': query}, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        results = data.get('results', {}).get('bindings', [])
        return [{
            'item': r.get('item', {}).get('value', ''),
            'itemLabel': r.get('itemLabel', {}).get('value', '')
        } for r in results]
    except Exception as e:
        print(f"Query error: {e}")
        return []


def cat_query(category):
    """Create SPARQL query to search humans inside a Wikipedia category"""
    return f'''SELECT ?item ?itemLabel WHERE {{
  BIND("{category}" as ?category)
  SERVICE wikibase:mwapi {{
     bd:serviceParam wikibase:endpoint "en.wikipedia.org";
                     wikibase:api "Generator";
                     mwapi:generator "categorymembers";
                     mwapi:gcmtitle ?category.
     ?item wikibase:apiOutputItem mwapi:item.
  }}
  FILTER BOUND (?item)
  FILTER EXISTS {{
    ?article schema:about ?item .
    ?item wdt:P31 wd:Q5.
  }}
SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}'''


def main():
    # Load filtered data
    if os.path.exists(f"{DATA_DIR}/3_wikicategories_distances_filtered.csv"):
        data = pd.read_csv(f"{DATA_DIR}/3_wikicategories_distances_filtered.csv")
    else:
        data = pd.read_csv(f"{DATA_DIR}/3_wikicategories_distances_filtered_rerun.csv")

    print(f"Loaded {len(data)} filtered categories")

    # Get unique category titles
    queries_titles = data['title'].unique().tolist()
    print(f"Querying {len(queries_titles)} unique categories")

    # Query Wikidata
    all_results = []
    for i, title in enumerate(queries_titles):
        if i % 50 == 0:
            print(f"Processing {i}/{len(queries_titles)}...")

        query = cat_query(title)
        results = query_wikidata(query)

        for r in results:
            r['category'] = title
            all_results.append(r)

    df_humans = pd.DataFrame(all_results)

    # Save results
    output_file = f"{DATA_DIR}/4_theorystrings_categories_humans.csv"
    df_humans.to_csv(output_file, index=False)
    print(f"Saved {len(df_humans)} results to {output_file}")

    # Get unique humans
    df_unique = df_humans.drop_duplicates(subset=['itemLabel']).copy()
    if 'category' in df_unique.columns:
        df_unique = df_unique.drop(columns=['category'])

    print(f"Unique humans: {len(df_unique)}")

    # Save unique humans
    unique_output_file = f"{DATA_DIR}/4_theorystrings_categories_humans_unique.csv"
    df_unique.to_csv(unique_output_file, index=False)
    print(f"Saved unique humans to {unique_output_file}")


if __name__ == "__main__":
    main()
