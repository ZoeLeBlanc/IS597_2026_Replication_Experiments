#!/usr/bin/env python3

"""
run_chapter2.py

A simplified script to run Chapter 2 genre classification models from Ted Underwood's
"Distant Horizons" book. This script fixes path issues in the original reproduce.py.

Usage:
    python run_chapter2.py locdetective
    python run_chapter2.py allSF
    python run_chapter2.py detectnewgatesensation
"""

import csv, os, sys, pickle, math
import pandas as pd

# Get the directory where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up to week3_code, then to original_project (parent of horizon)
WEEK3_DIR = os.path.dirname(SCRIPT_DIR)
ORIGINAL_PROJECT_DIR = os.path.join(WEEK3_DIR, 'original_project')
HORIZON_DIR = os.path.join(ORIGINAL_PROJECT_DIR, 'horizon')
LOGISTIC_DIR = os.path.join(HORIZON_DIR, 'logistic')

# Add paths so we can import horizon and its submodules
sys.path.insert(0, ORIGINAL_PROJECT_DIR)  # for 'import horizon'
sys.path.insert(0, LOGISTIC_DIR)  # for bare imports in logistic modules

from horizon.logistic import versatiletrainer as train

# Define paths relative to replication_code directory
# Data sourcefiles are stored locally in this project
SOURCEFOLDER = os.path.join(SCRIPT_DIR, 'data', 'sourcefiles')
# Metadata and lexicons come from Ted's horizon project
METADATAPATH = os.path.join(HORIZON_DIR, 'chapter2', 'metadata', 'concatenatedmeta.csv')
OUTPUTDIR = os.path.join(SCRIPT_DIR, 'model_output')
LEXICONDIR = os.path.join(HORIZON_DIR, 'lexicons')


def genre_gridsearch(modelname, c_range, ftstart, ftend, ftstep, positive_tags,
                     negative_tags=['random', 'grandom', 'chirandom'],
                     excl_below=1700, excl_above=2000,
                     metadatapath=None):
    """
    Perform grid search to find optimal feature count and regularization.
    Then produce that model and write it to disk.
    """

    if metadatapath is None:
        metadatapath = METADATAPATH

    sourcefolder = SOURCEFOLDER
    extension = '.tsv'
    vocabpath = os.path.join(LEXICONDIR, modelname + '.txt')

    if os.path.exists(vocabpath):
        print(f'Vocabulary for {modelname} already exists. Using it.')

    outputpath = os.path.join(OUTPUTDIR, modelname + '.csv')

    # Exclusion dictionaries
    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = excl_below
    excludeabove['firstpub'] = excl_above

    sizecap = 400

    testphrase = ''
    testconditions = set([x.strip() for x in testphrase.split(',') if len(x) > 0])

    datetype = "firstpub"
    numfeatures = ftend
    regularization = .000075

    paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

    print("Paths:")
    print(f"  Source folder: {sourcefolder}")
    print(f"  Metadata: {metadatapath}")
    print(f"  Output: {outputpath}")
    print(f"  Vocab: {vocabpath}")
    print()
    print(f"Exclusions: {exclusions}")
    print(f"Classify conditions: {classifyconditions}")

    modelparams = 'logistic', 10, ftstart, ftend, ftstep, c_range
    print(f"\nModel params: {modelparams}")
    print("\nStarting model training...")

    matrix, rawaccuracy, allvolumes, coefficientuples = train.tune_a_model(paths, exclusions, classifyconditions, modelparams)

    print(f'\nIf we divide the dataset with a horizontal line at 0.5, accuracy is: {rawaccuracy}')
    return rawaccuracy


def main():
    args = sys.argv

    if len(args) < 2:
        print("Usage: python run_chapter2.py <model_option>")
        print("\nAvailable options:")
        print("  locdetective      - Library of Congress detective fiction")
        print("  alldetective      - All detective fiction sources")
        print("  allSF             - All science fiction (Figure 2.2)")
        print("  detectnewgatesensation - Detective + Newgate + Sensation (Figure 2.1)")
        print("  allgothic         - All gothic fiction")
        print("  sensation         - Sensation fiction only")
        print("  newgateonly       - Newgate fiction only")
        sys.exit(1)

    option = args[1]

    if option == 'locdetective':
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst']
        c_range = [.001, .003, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 5250
        featurestep = 250
        genre_gridsearch('locdetective', c_range, featurestart, featureend, featurestep, positive_tags)

    elif option == 'alldetective':
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 3000
        featureend = 4400
        featurestep = 50
        genre_gridsearch('alldetective', c_range, featurestart, featureend, featurestep, positive_tags)

    elif option == 'allSF':
        positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, .6, 1, 8]
        featurestart = 2000
        featureend = 6000
        featurestep = 100
        genre_gridsearch('allSF', c_range, featurestart, featureend, featurestep, positive_tags)

    elif option == 'detectnewgatesensation':
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100', 'newgate', 'sensation']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2800
        featureend = 4400
        featurestep = 100
        genre_gridsearch('detectnewgatesensation', c_range, featurestart, featureend, featurestep, positive_tags)

    elif option == 'allgothic':
        positive_tags = ['stangothic', 'pbgothic', 'lochorror', 'locghost', 'chihorror']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch('allgothic', c_range, featurestart, featureend, featurestep, positive_tags)

    elif option == 'sensation':
        positive_tags = ['sensation']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 4800
        featurestep = 200
        genre_gridsearch('sensation', c_range, featurestart, featureend, featurestep, positive_tags)

    elif option == 'newgateonly':
        positive_tags = ['newgate']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 4800
        featurestep = 200
        genre_gridsearch('newgateonly', c_range, featurestart, featureend, featurestep, positive_tags)

    else:
        print(f"Unknown option: {option}")
        print("Run without arguments to see available options.")
        sys.exit(1)


if __name__ == '__main__':
    main()
