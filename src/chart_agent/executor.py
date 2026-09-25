import re
import matplotlib
matplotlib.use("Agg") # No GUI window for plot
import pandas as pd

_CODE_BLOCK_RE = re.compile(r"<execute_python>([\s\S]*?)</execute_python>")

def extract_code(llm_output: str) -> str | None:
    match = _CODE_BLOCK_RE.search(llm_output)
    return match.group(1).strip() if match else None


def run_chart_code(code: str, df: pd.DataFrame) -> None:
    exec_globals = {"df": df}
    exec(code, exec_globals)

