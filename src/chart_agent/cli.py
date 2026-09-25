"""Command-line entry point for the chart reflection workflow."""

import argparse
import logging

from dotenv import load_dotenv

from .workflow import run_workflow


def main() -> None:
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Generate a chart, reflect on it, and regenerate an improved version."
    )
    parser.add_argument("dataset", help="Path to the input CSV file")
    parser.add_argument("instruction", help="Natural-language description of the chart to create")
    parser.add_argument(
        "--model",
        default="gemini-3.8-flash",
        help="Gemini model used for both generation and reflection (default: %(default)s)",
    )
    parser.add_argument("--out-dir", default="outputs", help="Directory to save the generated charts")
    parser.add_argument("--basename", default="chart", help="Basename for the saved chart files")
    args = parser.parse_args()

    result = run_workflow(
        dataset_path=args.dataset,
        instruction=args.instruction,
        model=args.model,
        out_dir=args.out_dir,
        basename=args.basename,
    )

    print()
    print("Feedback:", result["feedback"])
    print("v1 chart:", result["v1_chart"])
    print("v2 chart:", result["v2_chart"])


if __name__ == "__main__":
    main()
