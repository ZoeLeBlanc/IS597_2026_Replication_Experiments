"""
Explore Theorists - Python replication of 5explore_theorists.R
"""
import pandas as pd
import os

# Set data directory
DATA_DIR = "../data"


def clean_names(df):
    """Clean column names: lowercase, replace spaces with underscores"""
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df


def main():
    # Check if extended data exists
    extended_file = f"{DATA_DIR}/4_theory_dictionary_wikidata_extended.csv"

    if os.path.exists(extended_file):
        data = pd.read_csv(extended_file)
        data = clean_names(data)
        print(f"Loaded extended data with {len(data)} rows")
        print(f"Columns: {data.columns.tolist()}")
    else:
        # Use the humans data we have
        humans_file = f"{DATA_DIR}/4_theorystrings_categories_humans.csv"
        data = pd.read_csv(humans_file)
        data = clean_names(data)
        print(f"Using humans data with {len(data)} rows")
        print(f"Columns: {data.columns.tolist()}")

    # Explore distinct items - eliminate duplicates
    if 'wikidata_id' in data.columns:
        unique_data = data.drop_duplicates(subset=['wikidata_id'])
        id_col = 'wikidata_id'
    elif 'item' in data.columns:
        unique_data = data.drop_duplicates(subset=['item'])
        id_col = 'item'
    else:
        unique_data = data.drop_duplicates(subset=['itemlabel'])
        id_col = 'itemlabel'

    print(f"\nUnique persons: {len(unique_data)}")

    # Explore genders if available
    if 'sex_or_gender' in unique_data.columns:
        print("\nGender distribution:")
        print(unique_data['sex_or_gender'].value_counts())

    # Explore countries if available
    if 'country_of_citizenship' in unique_data.columns:
        print("\nTop countries of citizenship:")
        print(unique_data['country_of_citizenship'].value_counts().head(20))

    # Summary statistics
    print("\n=== Summary ===")
    print(f"Total records: {len(data)}")
    print(f"Unique persons: {len(unique_data)}")

    if 'category' in data.columns:
        print(f"Unique categories: {data['category'].nunique()}")

        # Top categories by number of persons
        print("\nTop categories by person count:")
        print(data.groupby('category').size().sort_values(ascending=False).head(10))


if __name__ == "__main__":
    main()
