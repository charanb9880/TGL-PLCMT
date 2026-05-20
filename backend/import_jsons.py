import os
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(".env")
engine = create_engine(os.environ["DATABASE_URL"])

json_dir = "/app/research_outputs"
json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]

data = []
for f in json_files:
    try:
        with open(f, 'r') as file:
            content = json.load(file)
            if "golden_record" in content:
                data.append(content["golden_record"])
            else:
                data.append(content)
    except Exception as e:
        print(f"Error reading {f}: {e}")

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

with engine.connect() as conn:
    res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'company'"))
    valid_cols = [r[0] for r in res.fetchall()]

# Drop columns not in valid_cols
for col in df.columns:
    if col not in valid_cols:
        df = df.drop(columns=[col])

# Fill missing columns with None
for col in valid_cols:
    if col not in df.columns and col != "company_id":
        df[col] = None

# Reorder columns to match valid_cols (excluding company_id)
cols_to_insert = [c for c in valid_cols if c != "company_id"]
df = df[cols_to_insert]

for col in df.columns:
    df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x)

df.to_sql("company", engine, if_exists="append", index=False)
print(f"Successfully inserted {len(df)} companies from JSONs!")
