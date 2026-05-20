import pytest
import json
import os
import sys
import pandas as pd

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(__file__))

def load_from_excel(file_path):
    if not os.path.exists(file_path):
        return []
    
    excel_file = pd.ExcelFile(file_path)
    combined_data = []
    
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        if df.empty: continue
        
        records = df.to_dict(orient="records")
        for record in records:
            record["rule_id"] = sheet_name
            # Handle JSON input
            if "Input Data" in record and isinstance(record["Input Data"], str):
                try:
                    record["parsed_input"] = json.loads(record["Input Data"])
                except:
                    record["parsed_input"] = {}
            else:
                record["parsed_input"] = record.get("Input Data", {})
        combined_data.extend(records)
    return combined_data

@pytest.fixture(scope="session")
def test_data():
    path = os.path.join(os.path.dirname(__file__), "data", "Test_cases.xlsx")
    return load_from_excel(path)

@pytest.fixture(scope="session")
def rules_config():
    path = os.path.join(os.path.dirname(__file__), "rules", "rules.json")
    with open(path, "r") as f:
        return json.load(f)
