"""
Query Wikipedia - Python replication of 2_query_wikipedia.py (updated)
"""
import requests
import pandas as pd
import os

# Set data directory
DATA_DIR = "../data"


def query_wikipedia_categories(query_string):
    """Query Wikipedia API for categories matching the query string"""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'utf8': 1,
        'srsearch': query_string,
        'srnamespace': 14  # Category namespace
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        search_results = data.get('query', {}).get('search', [])
        return search_results
    except Exception as e:
        print(f"Error querying '{query_string}': {e}")
        return []


def main():
    # Get file with all "theory of strings"
    if os.path.exists(f"{DATA_DIR}/1_theoriesof_complete.csv"):
        string_filename = f"{DATA_DIR}/1_theoriesof_complete.csv"
    else:
        string_filename = f"{DATA_DIR}/1_theoriesof_complete_rerun.csv"

    # Read with pandas
    df = pd.read_csv(string_filename)
    print(f"Loaded {len(df)} theory strings from {string_filename}")

    # Get all strings as a list
    query_strings = df["normalized_string"].dropna().tolist()

    # Query Wikipedia and collect results
    all_results = []
    for i, query_string in enumerate(query_strings):
        if i % 100 == 0:
            print(f"Processing {i}/{len(query_strings)}...")

        results = query_wikipedia_categories(query_string)
        for result in results:
            result['query_string'] = query_string
            all_results.append(result)

    # Create DataFrame from results
    all_results_df = pd.DataFrame(all_results)
    print(f"Retrieved {len(all_results_df)} category matches")

    # Create column "category" with category name without "Category:" string
    if 'title' in all_results_df.columns:
        all_results_df["category"] = all_results_df["title"].str.replace("Category:", "", regex=False)

    # Save results in csv
    output_file = f"{DATA_DIR}/2_wikipediacategoriesfromquery.csv"
    all_results_df.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()
