# Chart Reflection Agent

An agentic workflow that applies the **reflection pattern** to data visualization:

1. **Generate (V1)** — an LLM writes matplotlib code for a chart from a natural-language instruction.
2. **Execute** — the code is extracted and run against the dataset to produce a chart image.
3. **Reflect** — a vision-capable LLM looks at the V1 chart image plus the original code, and critiques it against the instruction.
4. **Regenerate (V2)** — the LLM rewrites the code based on its own critique, which is executed to produce an improved chart.


## Project layout

```
src/chart_agent/
  data.py        # CSV loading + schema summarization for prompts
  generator.py    # V1 prompt + code generation
  executor.py      # extracts <execute_python> code and runs it against df
  reflector.py     # sends the chart image + code to a vision model for critique + V2 code
  providers.py     # Gemini client wiring
  workflow.py       # orchestrates the full generate -> execute -> reflect -> execute loop
  cli.py            # `chart-agent` command-line entry point
examples/run_example.py  # scripted end-to-end example
tests/                     # unit tests (no network calls)
sample_data/coffee_sales.csv
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
# then edit .env and set GOOGLE_API_KEY
```

## Usage

### CLI

```bash
chart-agent sample_data/coffee_sales.csv \
  "Compare total sales by coffee type between 2024 and 2025" \
  --model gemini-3.8-flash \
  --basename drink_sales
```

Charts are written to `outputs/<basename>_v1.png` and `outputs/<basename>_v2.png`.

### Library

```python
from chart_agent import run_workflow

result = run_workflow(
    dataset_path="sample_data/coffee_sales.csv",
    instruction="Compare total sales by coffee type between 2024 and 2025",
    model="gemini-3.8-flash",
    basename="drink_sales",
)

print(result["feedback"])
```

### Example script

```bash
python examples/run_example.py
```

## Testing

```bash
pytest
```

