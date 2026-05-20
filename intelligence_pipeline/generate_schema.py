import pandas as pd
import re

def sanitize_name(name):
    # Convert string to valid python identifier (alphanumeric and underscore)
    clean = re.sub(r'[^0-9a-zA-Z_]', '_', str(name))
    # Cannot start with number
    if re.match(r'^[0-9]', clean):
        clean = "f_" + clean
    return clean

xl = pd.ExcelFile('/Users/charanb/Desktop/TGL_Customised/TGl.xlsx')
df = xl.parse('Twitter_Consolidated')
params = df['Parameter'].dropna().tolist()

schema_code = "from pydantic import BaseModel, Field\nfrom typing import Optional\n\nclass CompanyIntelligenceSchema(BaseModel):\n"
for p in params:
    field_name = sanitize_name(p)
    # We use Field(alias=...) so the generated JSON matches the exact string in the Excel file
    schema_code += f"    {field_name}: Optional[str] = Field(default=None, alias=\"{p}\", description=\"{p}\")\n"

with open('/Users/charanb/Desktop/TGL_Customised/final_ui/langgraph/schema.py', 'w') as f:
    f.write(schema_code)

print("Schema generated successfully!")
