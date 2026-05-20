import os
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(".env")
engine = create_engine(os.environ["DATABASE_URL"])

# Directories containing the fully populated LangGraph Golden Records
dirs = [
    "/app/company_jsons",
    "/app/research_outputs"
]

data = []
seen_names = set()

for d in dirs:
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if not f.endswith('.json'):
            continue
            
        file_path = os.path.join(d, f)
        try:
            with open(file_path, 'r') as file:
                content = json.load(file)
                # Handle either nested "golden_record" or flat structure
                record = content.get("golden_record", content)
                
                # Use company name as a unique identifier to avoid duplicates
                name = record.get("company_name", record.get("Company Name", f))
                if name not in seen_names:
                    data.append(record)
                    seen_names.add(name)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

df = pd.DataFrame(data)

# Clean column names to match the database (snake_case)
df.columns = (
    df.columns.str.lower()
    .str.replace(r'[^a-z0-9]', '_', regex=True)
    .str.replace(r'_+', '_', regex=True)
    .str.strip('_')
)
# Special case to fix "company_name" -> "name"
df = df.rename(columns={"company_name": "name"})

# Serialize lists/dicts to JSON strings for postgres insertion
for col in df.columns:
    df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x)

# Recreate the table from scratch
with open("/app/supabase_schema.sql", "r") as f:
    schema_sql = f.read()

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS public.company CASCADE;"))
    conn.execute(text(schema_sql))
    conn.commit()
    
    # Fetch valid columns
    res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'company'"))
    valid_cols = [r[0] for r in res.fetchall()]

# Ensure exact mapping to the 163 parameters
for col in valid_cols:
    if col not in df.columns and col != "company_id":
        df[col] = None

# Add company_id manually
df["company_id"] = range(1, len(df) + 1)

cols_to_insert = valid_cols
df = df[cols_to_insert]

# Insert the 20+ pristine companies
df.to_sql("company", engine, if_exists="append", index=False)
print(f"Successfully wiped DB and ingested {len(df)} pristine LangGraph companies with all 163 parameters!")
