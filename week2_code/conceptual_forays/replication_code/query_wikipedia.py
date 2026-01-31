"""
Query Wikipedia - Python replication of 2_query_wikipedia.py (updated)
"""
import requests
import pandas as pd
import os

def get_file_path(filename):
    """Get path to data file. Rerun files stay in replication_code/data, others prefer original_project/data"""
    original_data = os.path.join(os.path.dirname(__file__), "original_project", "data")
    rerun_data = os.path.join(os.path.dirname(__file__), "data")

    # If filename contains "rerun", use replication_code/data
    if "rerun" in filename.lower():
        return os.path.join(rerun_data, filename)

    # Otherwise, prefer original_project/data, fall back to replication_code/data
    original_path = os.path.join(original_data, filename)
    if os.path.exists(original_path):
        return original_path
    return os.path.join(rerun_data, filename)

# For backwards compatibility, set DATA_DIR to the base directory we'll use
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


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
    if os.path.exists(get_file_path("1_theoriesof_complete.csv")):
        string_filename = get_file_path("1_theoriesof_complete.csv")
    else:
        string_filename = get_file_path("1_theoriesof_complete_rerun.csv")

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
    output_file = get_file_path("2_wikipediacategoriesfromquery.csv")
    all_results_df.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()
