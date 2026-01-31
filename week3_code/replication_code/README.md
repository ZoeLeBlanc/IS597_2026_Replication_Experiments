# Replication Code: Chapter 2 Genre Classification

This directory contains the working code and data for replicating Ted Underwood's Chapter 2 genre classification study using machine learning on 19th-century literary texts.

## Files & Directories

### Core Scripts

- **`run_chapter2.py`** - Main training script
  - Runs logistic regression models to classify literary genres
  - Performs grid search over regularization parameters
  - Outputs predictions, coefficients, and serialized models
  - Usage: `python3 run_chapter2.py [model_option]`

### Data

- **`data/sourcefiles/`** - 1,049 TSV files containing word frequency counts
  - Each file represents one volume from HathiTrust
  - Format: word \t count (tab-separated)
  - Generated from raw OCR texts

### Results

- **`model_output/`** - Generated outputs from model training
  - `{modelname}.csv` - Predictions and metadata for all texts
  - `{modelname}.coefs.csv` - Feature coefficients (word importance scores)
  - `{modelname}.pkl` - Serialized scikit-learn model object

### Analysis

- **`Chapter2ReplicationStudy.ipynb`** - Jupyter notebook with visualizations
  - 5 interactive Altair visualizations
  - Performance metrics (accuracy, precision, recall, F1)
  - Feature importance analysis
  - Temporal trend analysis

### Configuration

- **`lexicons/`** - Feature vocabulary files (5,251 words)
  - Lists the words used as features in the model
  - Shared across all models for consistency

## Running an Experiment

### Single Model Training

```bash
python3 run_chapter2.py locdetective
```

This will:
1. Load 1,048 volumes from metadata
2. Extract 5,251 features (word counts)
3. Perform 10-fold cross-validation
4. Grid search over 10 regularization parameters
5. Save results to `model_output/locdetective.*`

### View Results

Open `Chapter2ReplicationStudy.ipynb` and set:

```python
model_name = 'locdetective'  # Change this to your model
```

Then run all cells to generate visualizations.

## Model Options

| Model | Positive Classes | Description |
|-------|-----------------|-------------|
| `locdetective` | locdetective, locdetmyst, chimyst | Library of Congress detective fiction |
| `alldetective` | + det100 | All detective fiction sources |
| `allSF` | locscifi, anatscifi, femscifi, chiscifi | All science fiction (Figure 2.2) |
| `detectnewgatesensation` | + newgate, sensation | Detective + Newgate + Sensation (Figure 2.1) |
| `allgothic` | stangothic, pbgothic, lochorror, locghost, chihorror | All gothic fiction |
| `sensation` | sensation | Sensation fiction only |
| `newgateonly` | newgate | Newgate fiction only |

## Understanding the Output

### predictions CSV

Columns:
- `volid` - HathiTrust volume ID
- `logistic` - Predicted probability (0 to 1)
- `realclass` - Actual class (0 = not genre, 1 = genre)
- `trainflag` - 1 if in training set, 0 if test set
- `firstpub` - Publication year
- `title`, `author` - Bibliographic data
- `genretags` - Genre tags from metadata

### coefficients CSV

Columns:
- `word` - Feature word
- `coefficient` - L2-regularized weight (larger = stronger signal for genre)
- `impact` - Impact magnitude (absolute value of coefficient)

Positive coefficients indicate words that appear more in the target genre.
Negative coefficients indicate words more common in non-genre texts.

## Performance Metrics

Example output from `detectnewgatesensation` model:

```
Overall Accuracy: 92.5%
Precision: 93.2%
Recall: 91.8%
F1-Score: 92.5%
```

These are cross-validated scores (test set accuracy averaged across 10 folds).

## Technical Details

- **Algorithm**: L2-regularized Logistic Regression (scikit-learn)
- **Cross-validation**: 10-fold, with author-based grouping to prevent data leakage
- **Temporal filtering**: Models exclude volumes outside 1700-2000 range
- **Feature selection**: Top 5,251 words by document frequency
- **Negative class**: Random control texts + other genre controls

## Metadata Source

All metadata and vocabulary files are pulled from Ted's horizon project (../original_project/horizon/), which includes:
- `chapter2/metadata/concatenatedmeta.csv` - 1,048 volumes with tags
- `lexicons/` - Feature vocabulary for all models

The data in this directory (`data/sourcefiles/`) is independent and used for training.

## Dependencies

See `../environment/requirements.txt`:
- pandas
- numpy
- scikit-learn
- matplotlib
- altair

Install with: `pip install -r ../environment/requirements.txt`
