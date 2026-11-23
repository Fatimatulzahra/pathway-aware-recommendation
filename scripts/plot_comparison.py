from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"


def main():
    relevance = pd.read_csv(TABLES / "relevance_metrics_summary.csv")
    breadth = pd.read_csv(TABLES / "comparison_metrics_summary.csv")

    methods = ["keyword", "tfidf"]
    names = ["Keyword", "TF-IDF"]
    colors = ["#466782", "#218579"]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    fig.suptitle(
        "Preliminary recommendation comparison",
        fontsize=16,
        fontweight="bold",
    )

    # Panel 1: compare relevance measures at the judged list size.
    positions = np.arange(2)
    width = 0.34

    for index, method in enumerate(methods):
        row = relevance.set_index("method").loc[method]
        values = [
            row["precision_at_5"],
            row["pooled_ndcg_at_5"],
        ]

        bars = axes[0].bar(
            positions + (index - 0.5) * width,
            values,
            width,
            label=names[index],
            color=colors[index],
        )
        axes[0].bar_label(bars, fmt="%.3f", padding=4, fontsize=9)

    axes[0].set_xticks(
        positions, ["Precision@5", "Pooled nDCG@5"]
    )
    axes[0].set_ylim(0, 1.1)
    axes[0].set_ylabel("Mean score")
    axes[0].set_title("Interest relevance across 12 profiles")
    axes[0].legend(loc="lower left")

    # Panel 2: coverage is measured separately for each list size.
    for index, method in enumerate(methods):
        selected = breadth[breadth["method"] == method].sort_values("k")
        percentages = selected["mean_pathway_coverage"] * 100

        axes[1].plot(
            selected["k"],
            percentages,
            marker="o",
            linewidth=2,
            color=colors[index],
            label=names[index],
        )

        for k, percentage in zip(selected["k"], percentages):
            axes[1].annotate(
                f"{percentage:.1f}%",
                (k, percentage),
                xytext=(0, (12 if index == 0 else -18) if k == 5 else (-18 if index == 0 else 12)),
                textcoords="offset points",
                ha="center",
                fontsize=9,
            )

    axes[1].set_xticks([5, 10, 20])
    axes[1].set_xlabel("Requested list size (k)")
    axes[1].set_ylabel("Mean pathway coverage (%)")
    axes[1].set_ylim(0, 60)
    axes[1].set_title("Breadth across 12 profiles")
    axes[1].legend(loc="upper left")

    for axis in axes:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.2)
        axis.set_axisbelow(True)

    fig.text(
        0.5,
        0.025,
        "Synthetic profiles;\n"
        "Relevance judged only at k=5. At k=20, lists averaged 16.58 results.",
        ha="center",
        fontsize=9,
        color="#444444",
    )

    fig.tight_layout(rect=[0, 0.12, 1, 0.92])
    FIGURES.mkdir(parents=True, exist_ok=True)

    output = FIGURES / "keyword_tfidf_comparison.png"
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved comparison figure to: {output}")


if __name__ == "__main__":
    main()