"""
Preprocessing Data - Python replication of 1preprocessingdata.R
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
    """Clean column names: lowercase, replace spaces/special chars with underscores"""
    df = df.copy()
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(' ', '_', regex=False)
        .str.replace('.', '_', regex=False)
        .str.replace('*', '', regex=False)
        .str.strip('_')
    )
    return df


def main():
    # Read data
    jjtheory = pd.read_csv(get_file_path("1_JJ_theor_.csv"))
    nntheory = pd.read_csv(get_file_path("1_NN_theor_.csv"))
    theory = pd.read_csv(get_file_path("1_theor_of_normalized.csv"))

    print(f"JJ Theory shape: {jjtheory.shape}")
    print(f"NN Theory shape: {nntheory.shape}")
    print(f"Theory shape: {theory.shape}")

    # Clean column names
    jjtheory = clean_names(jjtheory)
    nntheory = clean_names(nntheory)
    theory = clean_names(theory)

    print("After cleaning:")
    print(f"JJ Theory columns: {jjtheory.columns.tolist()}")
    print(f"NN Theory columns: {nntheory.columns.tolist()}")
    print(f"Theory columns: {theory.columns.tolist()}")

    # Rename columns for consistency
    jjtheory = jjtheory.rename(columns={'clustered_jj_theor': 'clustered_string', 'token_count': 'freq'})
    nntheory = nntheory.rename(columns={'clustered_nn_theor': 'clustered_string', 'token_count': 'freq'})
    theory = theory.rename(columns={'_': 'index'})

    # Join all "theories of" strings using full outer join
    theoriesof = pd.merge(
        theory[['normalized_string', 'freq']],
        jjtheory,
        left_on='normalized_string',
        right_on='clustered_string',
        how='outer',
        suffixes=('_theory', '_jj')
    )

    theoriesof = pd.merge(
        theoriesof,
        nntheory,
        left_on='normalized_string',
        right_on='clustered_string',
        how='outer',
        suffixes=('', '_nn')
    )

    # Fill normalized_string with values from clustered_string columns where null
    theoriesof['normalized_string'] = (
        theoriesof['normalized_string']
        .fillna(theoriesof['clustered_string'])
    )
    if 'clustered_string_nn' in theoriesof.columns:
        theoriesof['normalized_string'] = theoriesof['normalized_string'].fillna(theoriesof['clustered_string_nn'])

    # Unite freq columns
    freq_cols = [col for col in theoriesof.columns if 'freq' in col.lower()]
    theoriesof['combined_freq'] = theoriesof[freq_cols].fillna('').astype(str).agg('|'.join, axis=1)
    theoriesof['combined_freq'] = theoriesof['combined_freq'].str.replace(r'\|+', '|', regex=True).str.strip('|')

    # Count normalized strings
    print("\nCount of normalized strings:")
    print(theoriesof['normalized_string'].value_counts().head(20))

    # Filter unique "theories of" strings
    unique_theoriesof = theoriesof[['normalized_string']].drop_duplicates()
    print(f"\nUnique theories of: {len(unique_theoriesof)}")

    # Write csv with unique "theor* of" strings
    output_file = get_file_path("1_theoriesof_complete_rerun.csv")
    unique_theoriesof.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")

    # Compare different "theor* of" sets
    jj_orig = pd.read_csv(get_file_path("1_JJ_theor_.csv"))
    nn_orig = pd.read_csv(get_file_path("1_NN_theor_.csv"))
    theory_orig = pd.read_csv(get_file_path("1_theor_of_normalized.csv"))

    set_A = set(jj_orig.iloc[:, 0].dropna().str.strip())
    set_B = set(nn_orig.iloc[:, 0].dropna().str.strip())
    set_C = set(theory_orig['normalized_string'].dropna().str.strip())

    myl = {'A (JJ)': set_A, 'B (NN)': set_B, 'C (theory)': set_C}

    # Find differences - items unique to each set
    differences = {}
    for k, v in myl.items():
        other_sets = [s for name, s in myl.items() if name != k]
        differences[k] = v - set.union(*other_sets)

    print("\nSet differences:")
    for k, v in differences.items():
        print(f"Unique to {k}: {len(v)} items")


if __name__ == "__main__":
    main()
