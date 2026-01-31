"""
Explore Theorists - Python replication of 5explore_theorists.R
"""
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


def clean_names(df):
    """Clean column names: lowercase, replace spaces with underscores"""
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df


def main():
    # Check if extended data exists
    extended_file = get_file_path("4_theory_dictionary_wikidata_extended.csv")

    if os.path.exists(extended_file):
        data = pd.read_csv(extended_file)
        data = clean_names(data)
        print(f"Loaded extended data with {len(data)} rows")
        print(f"Columns: {data.columns.tolist()}")
    else:
        # Use the humans data we have
        humans_file = get_file_path("4_theorystrings_categories_humans.csv")
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
