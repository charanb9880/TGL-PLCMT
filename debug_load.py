import pandas as pd
import os
import logging

def load_tgl_data():
    file_path = "/Users/charanb/Desktop/TGL_Customised/TGl.xlsx"
    if not os.path.exists(file_path):
        return []
    
    xl = pd.ExcelFile(file_path)
    sheets = [s for s in xl.sheet_names if 'Consolidated' in s]
    
    combined_data = []
    for sheet in sheets:
        try:
            df = xl.parse(sheet)
            param_col = next((c for c in df.columns if 'Parameter' in str(c)), None)
            data_col = next((c for c in df.columns if 'Research Output' in str(c) or 'Data' in str(c)), None)
            
            if param_col and data_col:
                df = df.dropna(subset=[param_col])
                record = dict(zip(df[param_col].astype(str).str.strip(), df[data_col]))
                combined_data.append({
                    "company_sheet": sheet,
                    "record": record
                })
        except Exception as e:
            print(f"Failed to parse sheet {sheet}: {e}")
            
    return combined_data

data = load_tgl_data()
print(f"Loaded {len(data)} companies")
for d in data:
    print(f"Company Sheet: {d['company_sheet']}, Keys: {len(d['record'])}")
