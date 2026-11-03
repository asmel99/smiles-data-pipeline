# 🧪 SMILES Data Pipeline

A lightweight, robust Python toolkit designed to ingest, validate, canonicalize, and filter raw chemical datasets using **RDKit** and **Pandas**. Built for cheminformatics research pipelines and freelance chemical data compilation.

## Features
* **SMILES Validation:** Automatically catches and discards malformed or invalid SMILES strings using RDKit.
* **Canonicalization:** Standardizes molecular representations using RDKit (`isomericSmiles=True`).
* **De-duplication:** Removes duplicate compounds based on canonical structures.
* **ChEMBL Integration (NEW):** Automated REST API fetching of biological activity data (e.g., MIC) for specific target organisms.
* **Biological Data Cleaning (NEW):** Filters mixed units (µM, µg/mL), handles inexact relations (`>`, `<`), and aggregates duplicate experimental results using median MIC values.
* **Data Engineering Ready:** Easily extensible for property calculations (Molecular Weight, LogP, etc.).
## Requirements
* Python 3.8+
* Pandas
* RDKit (`conda install -c conda-forge rdkit`)

## Usage
```python
from pipeline import clean_and_standardize_smiles

clean_and_standardize_smiles("raw_data.csv", "clean_data.csv", smiles_col="SMILES")
