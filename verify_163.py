import json
import sys
import os

# Add the langgraph directory to path for imports
sys.path.append(os.path.join(os.getcwd(), 'langgraph'))

from schema import CompanyIntelligenceSchema

def verify_163_fields(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    schema_fields = [field.alias for field in CompanyIntelligenceSchema.model_fields.values()]
    
    missing = [f for f in schema_fields if f not in data]
    extra = [f for f in data if f not in schema_fields]
    
    print(f"Total Schema Fields: {len(schema_fields)}")
    print(f"Fields in JSON: {len(data)}")
    print(f"Missing Fields: {len(missing)}")
    if missing:
        print(f"Missing field samples: {missing[:5]}")
    
    print(f"Extra Fields: {len(extra)}")
    if extra:
        print(f"Extra field samples: {extra}")

    if len(missing) == 0:
        print("\n✅ SUCCESS: All 163+ schema parameters are present in the JSON.")
    else:
        print("\n❌ FAILURE: Missing parameters detected.")

if __name__ == "__main__":
    verify_163_fields('research_outputs/zomato_intelligence.json')
