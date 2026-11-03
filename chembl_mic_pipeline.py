import requests
import pandas as pd
import time

def fetch_chembl_mic_data(target_chembl_id):
    """
    Fetches raw MIC data from the ChEMBL API for a specific organism.
    """
    print(f"Fetching raw MIC activities for {target_chembl_id}...")
    base_url = "https://www.ebi.ac.uk/chembl/api/data/activity.json"
    params = {'target_chembl_id': target_chembl_id, 'standard_type': 'MIC', 'limit': 1000, 'offset': 0}
    
    all_activities = []
    while True:
        response = requests.get(base_url, params=params)
        if response.status_code != 200: break
        data = response.json()
        activities = data.get('activities', [])
        if not activities: break
        all_activities.extend(activities)
        params['offset'] += params['limit']
        time.sleep(0.2)
        
    df = pd.DataFrame(all_activities)
    cols = ['molecule_chembl_id', 'standard_value', 'standard_units', 'standard_relation']
    return df[[c for c in cols if c in df.columns]]

def clean_mic_data(df, threshold=32):
    """
    Cleans raw MIC data by handling units, removing inexact relations, 
    and creating binary labels (Active/Inactive).
    """
    print(f"Cleaning raw data. Initial rows: {len(df)}")
    
    # 1. Drop missing values
    df = df.dropna(subset=['standard_value'])
    
    # 2. Keep only exact measurements ('=') and standard units
    df = df[df['standard_relation'] == '=']
    df = df[df['standard_units'].isin(['uM', 'ug.mL-1'])]
    
    # 3. Convert values to numeric and take the median for duplicates
    df['standard_value'] = pd.to_numeric(df['standard_value'])
    df = df.groupby(['molecule_chembl_id', 'standard_units'])['standard_value'].median().reset_index()
    
    # 4. Create binary labels (1 = Active, 0 = Inactive)
    df['label'] = df['standard_value'].apply(lambda x: 1 if x <= threshold else 0)
    
    print(f"Cleaned data. Final unique compounds: {len(df)}")
    return df

if __name__ == "__main__":
    # Example: Bacillus subtilis (CHEMBL359)
    TARGET_ID = 'CHEMBL359'
    
    raw_df = fetch_chembl_mic_data(TARGET_ID)
    clean_df = clean_mic_data(raw_df, threshold=32)
    
    clean_df.to_csv(f'{TARGET_ID}_clean_mic.csv', index=False)
    print(f"Saved to {TARGET_ID}_clean_mic.csv")
