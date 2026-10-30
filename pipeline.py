import pandas as pd
from rdkit import Chem

def clean_and_standardize_smiles(input_csv_path, output_csv_path, smiles_col="SMILES"):
    """
    Reads a raw CSV containing SMILES, validates them using RDKit, 
    canonicalizes the structures, removes duplicates, 
    and exports a clean dataset.
    """
    print(f"Loading data from {input_csv_path}...")
    df = pd.read_csv(input_csv_path)
    
    if smiles_col not in df.columns:
        raise ValueError(f"Column '{smiles_col}' not found in the CSV file.")
    
    initial_count = len(df)
    print(f"Initial raw entries: {initial_count}")
    
    valid_data = []
    invalid_count = 0
    
    for idx, row in df.iterrows():
        raw_smiles = row[smiles_col]
        
        # 1. Parse SMILES using RDKit
        mol = Chem.MolFromSmiles(str(raw_smiles))
        
        if mol is None:
            invalid_count += 1
            continue  # Skip invalid syntax
            
        # 2. Canonicalize SMILES to ensure uniform representation
        canonical_smi = Chem.MolToSmiles(mol, isomericSmiles=True)
        
        row_dict = row.to_dict()
        row_dict['Canonical_SMILES'] = canonical_smi
        valid_data.append(row_dict)

    df_clean = pd.DataFrame(valid_data)
    print(f"Filtered out {invalid_count} invalid SMILES structures.")
    
    # 3. Remove duplicate canonical SMILES
    before_dedup = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['Canonical_SMILES'])
    duplicates_removed = before_dedup - len(df_clean)
    print(f"Removed {duplicates_removed} duplicate entries.")
    
    # 4. Save the cleaned dataset
    df_clean.to_csv(output_csv_path, index=False)
    print(f"Success! Cleaned dataset saved to {output_csv_path} with {len(df_clean)} records.")
    
    return df_clean

if __name__ == "__main__":
    input_file = "raw_industrial_molecules.csv"
    output_file = "clean_industrial_molecules.csv"
    # cleaned_df = clean_and_standardize_smiles(input_file, output_file)
