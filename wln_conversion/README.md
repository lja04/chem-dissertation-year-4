# WLN Conversion Pipeline

This directory contains scripts used to convert chemical structures from
SMILES notation into Wiswesser Line Notation (WLN) at large scale, and to
merge the resulting WLN strings back into an existing compound dataset.

The workflow is designed for high-performance computing (HPC) environments
using SLURM and task farming, allowing efficient processing of very large
datasets (e.g. ~1 million compounds).

---

## Overview of the Workflow

The WLN conversion is performed in two main stages:

1. **Parallel WLN generation**
   - The input dataset is split into manageable chunks.
   - For each chunk, taskfarm command files and SLURM job scripts are generated.
   - Each task converts a SMILES string into a WLN string using a WLN writer
     executable.

2. **Dataset merging**
   - The generated WLN output is collected into a single results file.
   - WLN strings are matched back to the original dataset using SMILES as the key.
   - A new dataset is written that includes an additional `wln_string` column.

---

## Scripts

### 1. WLN Taskfarm and SLURM Generation Script

This script:
- Loads a cleaned input CSV containing SMILES strings
- Splits the dataset into fixed-size chunks
- Generates taskfarm command files to convert SMILES → WLN
- Creates corresponding SLURM job scripts for submission to an HPC cluster

The output of this step is a set of WLN result files, one per chunk.

---

### 2. WLN Merge Script

This script:
- Loads the combined WLN results
- Reads the original compound dataset
- Matches WLN strings back to compounds using the SMILES representation
- Writes a new CSV containing all original fields plus a `wln_string` column

If a WLN conversion is unavailable for a compound, the entry is marked as
`MISSING`.

---

## Input and Output

**Input**
- A cleaned compound dataset containing SMILES strings
- WLN conversion results produced by the taskfarm jobs

**Output**
- A final compound dataset with an additional WLN representation for each molecule

---

## Notes

- The pipeline is intended for batch execution on an HPC system.
- Chunking is used to control memory usage and job runtime.
- WLN conversion is performed using an external WLN writer tool.
- Progress messages are printed during merging to monitor long-running jobs.

---

This pipeline supports the broader project aim of comparing different chemical
line notations and assessing their impact on machine learning performance.
