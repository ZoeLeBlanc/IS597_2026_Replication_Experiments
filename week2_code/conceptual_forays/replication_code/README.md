# Replication Code

This directory contains:

- **original_project/** — A git submodule pointing to the original research
  repository by Kleymann et al. **Do not edit files inside this directory.**
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

## Running the Code

To run the replication scripts, ensure you have the required Python environment
set up as specified in the `environment/` directory. Then, you can execute the
scripts or the Jupyter notebook to replicate the analyses from the original study.

To install the required packages, you can use pip: `pip install -r ../environment/requirements.txt`