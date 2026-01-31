# Week 2 — Conceptual Forays Replication

This week's assignment replicates the research pipeline from:

> Gutierrez, S., Burghardt, M., Niekler, A., & Kleymann, R.
> "Conceptual Forays: A Corpus-based Study of 'Theory' in Digital Humanities
> Journals" (JoCA 2022 / DH 2022).

## Directory Layout

    conceptual_forays/
    ├── replication_code/
    │   ├── original_project/    <- git submodule (do not edit)
    │   ├── preprocessingdata.py
    │   ├── query_wikipedia.py
    │   ├── jac_distance_categories.py
    │   ├── search_wikidata.py
    │   ├── explore_theorists.py
    │   └── ReplicatingStudy.ipynb
    └── environment/             <- Python environment config

## Setup

1. Make sure the submodule is initialized:

       git submodule update --init --recursive

2. Install dependencies from `environment/` (e.g., `pip install -r
   environment/requirements.txt`).

3. Work through `ReplicatingStudy.ipynb` or run the individual `.py` scripts.

## Data Access

All data files are provided by the original project inside
`replication_code/original_project/data/`. The replication scripts reference
this path via relative imports.
