"""
Jaccard Distance for Categories - Python replication of 3jac_distance_categories.R
"""
import pandas as pd
import numpy as np
import textdistance
import os

# Set data directory
DATA_DIR = "../data"


def calculate_jaccard_qgram(s1, s2, q=3):
    """Calculate Jaccard distance using q-grams (similar to R stringdist with method='jaccard')"""
    if pd.isna(s1) or pd.isna(s2):
        return np.nan
    s1, s2 = str(s1).lower(), str(s2).lower()
    return 1 - textdistance.jaccard.normalized_similarity(s1, s2)


def calculate_levenshtein(s1, s2):
    """Calculate Levenshtein distance"""
    if pd.isna(s1) or pd.isna(s2):
        return np.nan
    return textdistance.levenshtein.distance(str(s1), str(s2))


def main():
    # Read categories retrieved from matching with "theory of" strings
    categories_wikipedia = pd.read_csv(f"{DATA_DIR}/2_wikipediacategoriesfromquery.csv")

    print(f"Columns: {categories_wikipedia.columns.tolist()}")
    print(f"Unique titles: {categories_wikipedia['title'].nunique()}")
    print(f"Unique query strings: {categories_wikipedia['query_string'].nunique()}")

    # Count number of categories by each "theory of" string
    catcountbystring = categories_wikipedia.groupby('query_string')['title'].nunique().reset_index()
    catcountbystring.columns = ['query_string', 'count']

    print("\nCategories count by query string:")
    print(catcountbystring.describe())

    # Delete "Category:" string to match and compare with query string
    categories_wikipedia['category'] = categories_wikipedia['title'].str.replace('Category:', '', regex=False)

    # Calculate Jaccard and Levenshtein distances
    print("\nCalculating distances (this may take a moment)...")

    categories_wikipedia['jac'] = categories_wikipedia.apply(
        lambda row: calculate_jaccard_qgram(row['category'], row['query_string']), axis=1
    )

    categories_wikipedia['lev'] = categories_wikipedia.apply(
        lambda row: calculate_levenshtein(row['category'], row['query_string']), axis=1
    )

    print("Distance calculations complete")

    # Category count
    cat_count = categories_wikipedia.groupby('category').size().reset_index(name='n')
    print(f"\nUnique categories: {len(cat_count)}")
    print("\nTop 20 categories:")
    print(cat_count.nlargest(20, 'n'))

    # Filter categories by Jaccard distance
    df_filtered = categories_wikipedia[categories_wikipedia['jac'] < 0.6].copy()
    print(f"\nAfter jac < 0.6 filter: {len(df_filtered)} rows")

    # Filter by strange keywords
    exclude_pattern = r'WikiProject|Wikipedia|[C|c]onspiracy|Christ|[M|m]ilitary|articles|journals|missing|Satanic|[T|t]errorism|abuse|backlog|Lists|albums'
    snippet_exclude = r'[C|c]onspiracy|[T|t]elevision|Nazis'

    df_filtered = categories_wikipedia[
        (categories_wikipedia['jac'] < 0.6) &
        (~categories_wikipedia['category'].str.contains(exclude_pattern, regex=True, na=False)) &
        (~categories_wikipedia['snippet'].str.contains(snippet_exclude, regex=True, na=False))
    ].copy()

    print(f"After filtering: {len(df_filtered)} rows")

    # Save filtered categories
    output_file = f"{DATA_DIR}/3_wikicategories_distances_filtered_rerun.csv"
    df_filtered.to_csv(output_file, index=False)
    print(f"Saved filtered categories to {output_file}")


if __name__ == "__main__":
    main()
