import logging
from pathlib import Path
from .data import load_dataset, describe_schema
from .generator import generate_chart_code
from .executor import extract_code, run_chart_code
from .reflector import reflect_and_refine

log = logging.getLogger("chart_agent")

def run_workflow(dataset_path: str, instruction: str, model: str, out_dir: str = "outputs", basename: str = "chart"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    v1_path = f"{out_dir}/{basename}_v1.png"
    v2_path = f"{out_dir}/{basename}_v2.png"

    # load data + build schema
    df = load_dataset(dataset_path)
    schema = describe_schema(df)
    log.info("Loaded %s (%d rows)", dataset_path, len(df))

    # step 1: generate + run v1
    raw_v1 = generate_chart_code(model, instruction, schema, v1_path)
    code_v1 = extract_code(raw_v1)
    run_chart_code(code_v1, df)
    log.info("v1 chart saved to %s", v1_path)

    # step 2: reflect on v1, generate + run v2
    feedback, raw_v2 = reflect_and_refine(model, v1_path, instruction, code_v1, schema, v2_path)
    log.info("Feedback: %s", feedback)

    code_v2 = extract_code(raw_v2)
    run_chart_code(code_v2, df)
    log.info("v2 chart saved to %s", v2_path)

    return {
        "v1_code": code_v1,
        "v1_chart": v1_path,
        "feedback": feedback,
        "v2_code": code_v2,
        "v2_chart": v2_path,
    }