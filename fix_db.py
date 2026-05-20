from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
engine = create_engine(os.environ["DATABASE_URL"])
with engine.connect() as conn:
    conn.execute(text("DELETE FROM public.company WHERE company_id NOT IN ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')"))
    conn.commit()
    res = conn.execute(text("SELECT company_id, name FROM public.company ORDER BY company_id ASC"))
    print("Remaining companies:")
    for r in res.fetchall():
        print(f"ID: {r[0]} | Name: {r[1]}")
