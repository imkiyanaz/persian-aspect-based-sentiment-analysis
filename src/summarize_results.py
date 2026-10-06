"""Print the aggregate results exported by the research notebook."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def main():
    baselines = pd.read_csv(RESULTS / "baseline_results_context_based.csv")
    report = pd.read_csv(RESULTS / "parsbert_classification_report.csv", index_col=0)
    cm = pd.read_csv(RESULTS / "parsbert_confusion_matrix.csv", index_col=0)

    print("Classical baselines")
    print(baselines.to_string(index=False))
    print("\nParsBERT classification report")
    print(report.to_string())
    print("\nParsBERT confusion matrix")
    print(cm.to_string())


if __name__ == "__main__":
    main()
