# Evaluating the Computational Efficiency of Chemical Notations in Transformer-Based Models

This repository contains the code and experiments for a dissertation project investigating how the choice of chemical line notation affects the computational efficiency and performance of transformer-based neural networks for IUPAC name prediction.

## Project Motivation

Chemical structures can be represented as linear strings using different notations, such as InChI, SMILES, and Wiswesser Line Notation (WLN). While these notations describe the same molecules, they vary greatly in length and structure.

Transformers process sequences with a computational cost that scales quadratically with sequence length (O(n²)). This project explores whether more compact notations, particularly WLN, reduce training cost and improve efficiency compared to SMILES and InChI, and whether this comes at the expense of model accuracy.

## Hypothesis

Shorter chemical notations produce fewer tokens after tokenisation, resulting in less computational work per training step.  
WLN is therefore expected to train faster than SMILES and InChI, though potentially with lower predictive accuracy.

## Chemical Notations Studied

- **InChI** – Highly structured and unambiguous, designed for chemical databases
- **SMILES** – Human-readable and widely used in cheminformatics and machine learning
- **WLN (Wiswesser Line Notation)** – Extremely compact legacy notation designed for early computers

WLN strings were generated from SMILES using tools developed by Blakey et al. (2024).

## Dataset Construction

- Raw data sourced from PubChem (~142 million molecules)
- Randomly sampled 10 million molecules as a working pool
- Diversity selection strategies:
  - MiniBatchKMeans for 25k and 100k datasets
  - FAISS similarity search for the 1M dataset
- Final datasets: 25k, 100k, and 1M molecules
- Each molecule represented using InChI, SMILES, and WLN

## Models Implemented

### Simple Baseline Model
A lightweight transformer encoder–decoder model used to demonstrate relative effects of notation choice.

- Character-level tokenisation
- Teacher forcing during training
- Greedy decoding
- Intentionally minimal stabilisation
- Used primarily for qualitative and efficiency comparisons

### Paper-Based Model
A larger, more robust transformer inspired by Handsel et al. (2021).

- Deeper encoder–decoder architecture
- Larger embeddings and more attention heads
- Dropout, positional encoding, attention masking
- Label smoothing and learning rate scheduling
- Gradient accumulation
- Beam search decoding
- Originally optimised for InChI-to-IUPAC translation

## Training Setup

- Data split: 90% training, 5% validation, 5% testing
- Epochs:
  - 25k & 100k datasets: 15 epochs
  - 1M dataset: 5 epochs
- For the 1M dataset, the test set was limited to 10k samples due to runtime constraints

## Key Results

- WLN consistently produced the shortest token sequences
- WLN models trained the fastest across all dataset sizes
- InChI models trained the slowest due to long input sequences
- Accuracy depended strongly on model architecture:
  - The paper-based model performed best on InChI
  - WLN and SMILES showed lower accuracy with this architecture
- Results support the hypothesis that shorter notations reduce computational cost, but do not guarantee higher accuracy

## Future Work

- Notation-specific hyperparameter optimisation
- Alternative tokenisation strategies (subword, word-level)
- Extension to other notations (SELFIES, SMARTS)
- More rigorous evaluation metrics (edit distance, confidence scores)
- Improved stabilisation of the baseline model
- Beam search decoding for the baseline model
- Analysis of convergence behaviour rather than fixed epoch counts

## References

- Handsel et al., *Journal of Cheminformatics*, 2021 – Translating InChI to IUPAC names using transformers
- Blakey et al., *Journal of Cheminformatics*, 2024 – Extraction and conversion of Wiswesser Line Notation
