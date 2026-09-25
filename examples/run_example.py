"""End-to-end example of the chart reflection workflow.

Requires the package to be installed (`pip install -e .`) and a
GOOGLE_API_KEY set in a .env file at the project root.

Run with: python examples/run_example.py
"""

import logging

from dotenv import load_dotenv

from chart_agent.workflow import run_workflow


def main() -> None:
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    result = run_workflow(
        dataset_path="sample_data/coffee_sales.csv",
        instruction="Compare total sales by coffee type between 2024 and 2025",
        model="gemini-3.8-flash",
        basename="drink_sales",
    )

    print()
    print("Feedback:", result["feedback"])
    print("v1:", result["v1_chart"])
    print("v2:", result["v2_chart"])


if __name__ == "__main__":
    main()
