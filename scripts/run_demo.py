import os
from pathlib import Path
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from winback_marketing_agents.pipeline import run_demo_pipeline


def main() -> None:
    metrics = run_demo_pipeline(ROOT / "outputs")
    print("Winback Marketing Agents demo complete.")
    print("")
    print("Topline metrics")
    for key, value in metrics.items():
        print(f"- {key}: {value}")
    print("")
    print("Artifacts written to outputs/:")
    print("- scored_customers.csv")
    print("- action_summary.csv")
    print("- metrics.csv")
    print("- BUSINESS_CASE.md")
    print("- DEMO_SUMMARY.md")
    print("- charts/")


if __name__ == "__main__":
    main()
