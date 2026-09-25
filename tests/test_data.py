import pandas as pd

from chart_agent.data import describe_schema, load_dataset


def test_load_dataset_derives_date_parts(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("date,value\n2024-01-15,10\n2024-07-01,20\n")

    df = load_dataset(str(csv_path))

    assert list(df["year"]) == [2024, 2024]
    assert list(df["quarter"]) == [1, 3]
    assert list(df["month"]) == [1, 7]


def test_load_dataset_without_date_column_skips_derived_fields(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a,b\n1,x\n2,y\n")

    df = load_dataset(str(csv_path))

    assert "year" not in df.columns
    assert "quarter" not in df.columns
    assert "month" not in df.columns


def test_describe_schema_lists_every_column():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})

    schema = describe_schema(df)

    assert f"- a ({df['a'].dtype})" in schema
    assert f"- b ({df['b'].dtype})" in schema
    assert "'x'" in schema and "'y'" in schema
