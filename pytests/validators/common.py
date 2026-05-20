import pandas as pd

def is_null_like(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return True
    return str(val).strip().lower() in ["n/a", "unknown", "", "nan", "null", "none", "-"]
