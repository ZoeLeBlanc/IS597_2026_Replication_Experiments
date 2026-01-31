# IS597 — Code Replication Seminar (2026)

This repository contains materials for IS597 Culture At Scale, a graduate seminar focused on
replicating computational research from published studies.

## Structure

Each week's assignment lives in its own directory (e.g., `week2_code/`).
Within each week, you will find:

- **replication_code/** — instructor-provided replication scripts and the
  original project (included as a git submodule).
- **environment/** — environment configuration files (requirements, etc.).

## Getting Started

After cloning, initialize submodules to fetch the original research code:

    git clone --recurse-submodules <repo-url>

Or, if already cloned:

    git submodule update --init --recursive
