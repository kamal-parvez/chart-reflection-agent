"""Dataset loading and schema summarization"""

import pandas as pd


# possible name for a date column across different CSVs
_DATE_CANDIDATES = ("date", "order_date", "timestamp", "created_at")


def load_dataset(csv_path: str) -> pd.DataFrame:
    # load csv into a dataframe
    df = pd.read_csv(csv_path)

    # find the date column if one exists
    date_col = next((c for c in _DATE_CANDIDATES if c in df.columns), None)

    if date_col:
        # parse to datetime, derive year/quarter/month
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce", format="mixed")
        df["year"] = df[date_col].dt.year
        df["quarter"] = df[date_col].dt.quarter
        df["month"] = df[date_col].dt.month

    return df


def describe_schema(df: pd.DataFrame, n_samples: int = 3) -> str:
    # build a short text summary of columns + sample values, for the LLM prompt
    lines = []
    for col, dtype in df.dtypes.items():
        sample_vals = df[col].dropna().unique()[:n_samples]
        sample_str = ", ".join(repr(v) for v in sample_vals)
        lines.append(f"- {col} ({dtype}): e.g. {sample_str}")

    return "\n".join(lines)





