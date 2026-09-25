import pandas as pd
import pytest

from chart_agent.executor import extract_code, run_chart_code


def test_extract_code_returns_the_block_between_tags():
    llm_output = "preamble\n<execute_python>\nx = 1\n</execute_python>\ntrailing"

    assert extract_code(llm_output) == "x = 1"


def test_extract_code_returns_none_when_no_tags_present():
    assert extract_code("no tags here") is None


def test_run_chart_code_executes_with_df_in_scope():
    df = pd.DataFrame({"value": [1, 2, 3]})

    run_chart_code("assert df['value'].sum() == 6", df)


def test_run_chart_code_raises_for_undefined_names():
    df = pd.DataFrame({"value": [1]})

    with pytest.raises(NameError):
        run_chart_code("undefined_name", df)
