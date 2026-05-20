import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
engine = create_engine(os.environ["DATABASE_URL"])

# Read the schema file
with open("supabase_schema.sql", "r") as f:
    schema_sql = f.read()

# Load only the first 10 valid rows
df = pd.read_excel("TGl.xlsx", sheet_name="companies").head(10)

with engine.connect() as conn:
    # Drop the corrupted table
    conn.execute(text("DROP TABLE IF EXISTS public.company CASCADE;"))
    
    # Run the user's proper schema
    conn.execute(text(schema_sql))
    conn.commit()

# Insert the clean data
df.to_sql("company", engine, if_exists="append", index=False)
print("Restored the 10 original companies into the clean schema!")

