# Week 2 — Conceptual Forays Replication

This week's assignment replicates the research pipeline from:

Kleymann, Rabea, Andreas Niekler, and Manuel Burghardt. “Conceptual Forays: A Corpus-Based Study of ‘Theory’ in Digital Humanities Journals.” *Journal of Cultural Analytics* 7, no. 4 (December 19, 2022).

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
