# Replication Code

This directory contains:

- **original_project/** — A git submodule pointing to the original research
  repository by Gutierrez et al. **Do not edit files inside this directory.**
  Any changes there will not be tracked by the course repository and will be
  lost when the submodule is updated.

- **Python replication scripts** (`.py` files) and **ReplicatingStudy.ipynb** —
  Course-provided translations of the original R pipeline into Python. These
  are the files you will read, run, and learn from.

## Initializing the Submodule

If `original_project/` is empty, run:

    git submodule update --init --recursive

## Data Paths

The replication scripts expect data at `original_project/data/`. Make sure the
submodule is initialized before running any code.
