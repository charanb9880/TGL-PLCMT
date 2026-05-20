import pandas as pd
import json
import os
import datetime

xl = pd.ExcelFile('/Users/charanb/Desktop/TGL_Customised/TGl.xlsx')
sheets = [s for s in xl.sheet_names if 'Consolidated' in s]

output_dir = '/Users/charanb/Desktop/TGL_Customised/final_ui/company_jsons'
os.makedirs(output_dir, exist_ok=True)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

for sheet in sheets:
    df = xl.parse(sheet)
    try:
        keys = df.iloc[:, 3].dropna().astype(str).tolist()
        values = df.iloc[:, 4].tolist()
        min_len = min(len(keys), len(values))
        record = dict(zip(keys[:min_len], values[:min_len]))
        
        clean_record = {k: ("" if pd.isna(v) else v) for k, v in record.items()}
        
        company_name = clean_record.get('Company Name', sheet.replace('_Consolidated', ''))
        if pd.isna(company_name) or not company_name:
            company_name = sheet.replace('_Consolidated', '')
            
        filename = f"{company_name.replace(' ', '_')}.json"
        
        with open(os.path.join(output_dir, filename), 'w') as f:
            json.dump(clean_record, f, indent=4, default=json_serial)
        print(f"Extracted JSON for {company_name}")
    except Exception as e:
        print(f"Skipping {sheet} due to error: {e}")
