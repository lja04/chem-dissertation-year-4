# Datasets

This directory contains the datasets used throughout this project for training and evaluating machine learning models on chemical data.

The datasets consist of collections of chemical compounds represented using multiple chemical line notations (e.g. InChI, SMILES, WLN), alongside associated target values used for modelling tasks. They are designed to support experiments investigating how different chemical representations affect model performance, training efficiency, and scalability.

Dataset sizes vary to allow comparison between small-scale experiments, intermediate training runs, and large-scale models. This enables systematic evaluation of how dataset size and input representation influence learning behaviour and predictive accuracy.

All data originate from publicly available chemical databases and have been processed to ensure consistency and suitability for machine learning workflows. Depending on the experiment, datasets may be filtered, cleaned, or subsampled prior to use.

These datasets support the broader aims of the project, including:
- Comparing traditional and legacy chemical line notations  
- Assessing the impact of representation length on neural network training  
- Evaluating scalability across increasing dataset sizes  

