import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extras import execute_values

from company_data import locate_workbook


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")
DATABASE_URL = os.environ.get("DATABASE_URL")
MAIN_SHEET = "companies"


def infer_postgres_type(series: pd.Series) -> str:
    sample = series.dropna()
    if sample.empty:
        return "TEXT"
    if pd.api.types.is_bool_dtype(sample):
        return "BOOLEAN"
    if pd.api.types.is_integer_dtype(sample):
        return "BIGINT"
    if pd.api.types.is_float_dtype(sample):
        return "DOUBLE PRECISION"
    if pd.api.types.is_datetime64_any_dtype(sample):
        return "TIMESTAMP"
    return "TEXT"


def normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    for column in normalized.columns:
        normalized[column] = normalized[column].apply(
            lambda value: value.to_pydatetime() if hasattr(value, "to_pydatetime") else value,
        )
    return normalized.where(pd.notnull(normalized), None)


def create_table_query(columns: list[str], frame: pd.DataFrame):
    column_defs = []
    for column in columns:
        pg_type = infer_postgres_type(frame[column])
        column_defs.append(
            sql.SQL("{} {}")
            .format(sql.Identifier(column), sql.SQL(pg_type))
        )

    return sql.SQL(
        "CREATE TABLE public.company ({})"
    ).format(sql.SQL(", ").join(column_defs))


def main() -> None:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is missing in backend/.env")

    workbook_path = locate_workbook()
    frame = pd.read_excel(workbook_path, sheet_name=MAIN_SHEET).head(10)
    frame = normalize_frame(frame)
    columns = list(frame.columns)
    records = frame.to_records(index=False).tolist()

    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS public.company")
            cursor.execute(create_table_query(columns, frame))

            insert_query = sql.SQL("INSERT INTO public.company ({}) VALUES %s").format(
                sql.SQL(", ").join(sql.Identifier(column) for column in columns),
            )
            insert_query_string = insert_query.as_string(connection).replace("%", "%%").replace("VALUES %%s", "VALUES %s")
            execute_values(cursor, insert_query_string, records, page_size=200)

        connection.commit()

    print(
        f"Imported {len(records)} rows and {len(columns)} columns from {workbook_path.name} into public.company",
    )


if __name__ == "__main__":
    main()