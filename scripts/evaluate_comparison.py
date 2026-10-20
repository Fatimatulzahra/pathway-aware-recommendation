import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from recommend import OpportunityRecommender, load_opportunities

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"


def main():
    opportunities = load_opportunities()
    model = OpportunityRecommender(opportunities)
    id_to_index = {
        opportunity["id"]: index
        for index, opportunity in enumerate(opportunities)
    }

    pathways = runpy.run_path(
        str(ROOT / "data" / "taxonomy.py")
    )["PATHWAYS"]

    rankings = pd.read_csv(
        TABLES / "recommendation_rankings.csv",
        keep_default_na=False,
    )
    runs = pd.read_csv(TABLES / "comparison_runs.csv")
    rows = []

    for run in runs.to_dict("records"):
        selected = rankings[
            (rankings["profile_id"] == run["profile_id"])
            & (rankings["method"] == run["method"])
            & (rankings["k"] == run["k"])
        ].sort_values("rank")

        ids = selected["opportunity_id"].tolist()
        indices = [id_to_index[opportunity_id] for opportunity_id in ids]
        n = len(indices)

        if n != run["returned_count"]:
            raise ValueError("Ranking rows do not match the run summary.")

        represented = {
            pathway
            for index in indices
            for pathway in opportunities[index].get("pathways", [])
        }

        unknown = represented - set(pathways)
        if unknown:
            raise ValueError(f"Unknown pathway labels: {unknown}")

        # Compare every distinct pair using one shared TF-IDF space
        # for both recommendation methods.
        diversity = np.nan
        if n >= 2:
            similarities = cosine_similarity(model.matrix[indices])
            pairs = similarities[np.triu_indices(n, k=1)]
            diversity = float(
                np.clip(1 - pairs.mean(), 0, 1)
            )

        rows.append({
            **run,
            "fill_rate": n / run["k"],
            "distinct_pathways": len(represented),
            "pathway_coverage": len(represented) / len(pathways),
            "text_diversity": diversity,
        })

    metrics = pd.DataFrame(rows)
    metrics.to_csv(
        TABLES / "comparison_metrics_by_profile.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary = metrics.groupby(
        ["method", "k"], as_index=False
    ).agg(
        profiles=("profile_id", "count"),
        mean_returned=("returned_count", "mean"),
        mean_fill_rate=("fill_rate", "mean"),
        mean_distinct_pathways=("distinct_pathways", "mean"),
        mean_pathway_coverage=("pathway_coverage", "mean"),
        mean_text_diversity=("text_diversity", "mean"),
        profiles_with_diversity=("text_diversity", "count"),
    )

    summary.to_csv(
        TABLES / "comparison_metrics_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nPRELIMINARY COMPARISON")
    print(summary.round(3).to_string(index=False))
    print("\nSaved per-profile metrics and summary to results/tables.")
    print("Coverage uses unverified seed labels.")
    print("Diversity measures text differences, not recommendation relevance.")


if __name__ == "__main__":
    main()