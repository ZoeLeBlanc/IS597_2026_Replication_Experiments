# Week 3: Distant Horizons - Genre Classification

This directory contains a replication study of Ted Underwood's Chapter 2 genre classification models from *Distant Horizons*. The work demonstrates how machine learning can identify literary genres through linguistic features in 19th-century English-language fiction.

## Directory Structure

```
week3_code/
├── original_project/
│   └── horizon/              # Ted Underwood's Distant Horizons (git submodule)
│       ├── chapter2/         # Chapter 2 genre classification data & models
│       │   ├── metadata/     # Volume metadata (concatenatedmeta.csv)
│       │   ├── sourcefiles/  # Raw text files
│       │   └── modeloutput/  # Pre-trained model outputs
│       ├── logistic/         # Logistic regression training tools
│       ├── lexicons/         # Vocabulary files for feature extraction
│       └── ...
├── replication_code/         # Our reproduction and analysis
│   ├── data/
│   │   └── sourcefiles/      # 1,049 text files for training
│   ├── model_output/         # Generated model predictions & coefficients
│   ├── lexicons/             # Feature vocabulary files
│   ├── run_chapter2.py       # Main script to train models
│   └── Chapter2ReplicationStudy.ipynb  # Visualization & analysis notebook
├── environment/
│   └── requirements.txt       # Python dependencies
└── README.md                  # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r environment/requirements.txt
```

Required packages:
- `numpy` - numerical computing
- `pandas` - data manipulation
- `scikit-learn` - machine learning models
- `matplotlib` - plotting
- `altair` - interactive visualizations

### 2. Train a Model

```bash
cd replication_code
python3 run_chapter2.py detectnewgatesensation
```

Available model options:

- `locdetective` - Library of Congress detective fiction
- `alldetective` - All detective fiction sources
- `allSF` - All science fiction (Figure 2.2 in the book)
- `detectnewgatesensation` - Detective + Newgate + Sensation (Figure 2.1)
- `allgothic` - All gothic fiction
- `sensation` - Sensation fiction only
- `newgateonly` - Newgate fiction only

### 3. Visualize Results

Open `Chapter2ReplicationStudy.ipynb` in Jupyter and run the cells to generate Altair visualizations including:
- Distribution of prediction scores
- Genre trends over time
- Top positive and negative feature words
- Confusion matrix
- Prediction scatter plots

## Git Submodule Setup

The `original_project/horizon/` directory is a **git submodule** pointing to Ted Underwood's Distant Horizons repository. This allows us to:
- Keep Ted's code in sync with his original repository
- Avoid duplicating large files
- Track which version of his code we're using

### Cloning This Repository

If you're cloning this repository for the first time, initialize the submodule:

```bash
git clone https://github.com/yourusername/is597_2026.git
cd is597_2026/week3_code
git submodule update --init --recursive
```

Or clone with submodules in one step:

```bash
git clone --recurse-submodules https://github.com/yourusername/is597_2026.git
```

### Working with the Submodule

**Check submodule status:**

```bash
git status
```

**Update to latest version of Horizon:**

```bash
cd original_project/horizon
git pull origin main
cd ../..
git add original_project/horizon
git commit -m "Update horizon submodule to latest version"
```

**View submodule configuration:**

```bash
cat .gitmodules
```

The submodule points to: `git@github.com:tedunderwood/horizon.git`

### Important Notes

- The `original_project/horizon/` directory is read-only in our workflow
- We use its metadata, lexicons, and code but train on our local `replication_code/data/`
- Changes to the submodule should be tracked with commits as shown above
- Do not modify files directly in `original_project/horizon/` unless updating the submodule
- The data is available as tar files in the original repository if needed at this link [https://github.com/tedunderwood/horizon/tree/master/chapter2/sourcefiles](https://github.com/tedunderwood/horizon/tree/master/chapter2/sourcefiles). If you download and extract them manually, place them in `replication_code/data/sourcefiles/`

## Key Findings

This replication studies how machine learning classifiers can distinguish literary genres based on word frequencies and textual features. The models achieve **91%+ accuracy** on cross-validation when classifying detective, sensation, and Newgate fiction against random control texts from 1700-2000.

## How It Works

1. **Data**: 1,048 19th-century texts with genre metadata from the HathiTrust Digital Library
2. **Features**: 5,251 words selected by document frequency across the corpus
3. **Model**: L2-regularized logistic regression trained with 10-fold cross-validation
4. **Evaluation**: Grid search over regularization parameters and feature counts

## Output Files

After training, each model generates:
- `{modelname}.csv` - Predictions for all texts with metadata
- `{modelname}.coefs.csv` - Feature coefficients (word weights)
- `{modelname}.pkl` - Serialized trained model

## References

- Underwood, Ted. *Distant Horizons: Digital Evidence and Literary Change*. University of Chicago Press, 2019.
- Chapter 2: "The Genres of Fiction" explores how statistical methods can identify genre boundaries
- Code: https://github.com/tedunderwood/horizon

## File Path Setup

The `run_chapter2.py` script automatically configures paths:
- **Data**: Points to `replication_code/data/sourcefiles/` (your local texts)
- **Metadata**: Uses Ted's `horizon/chapter2/metadata/concatenatedmeta.csv`
- **Vocabulary**: Uses vocabulary files in `horizon/lexicons/`
- **Output**: Saves results to `replication_code/model_output/`

This hybrid approach uses Ted's precompiled metadata and vocabulary while training on your local text copies.
