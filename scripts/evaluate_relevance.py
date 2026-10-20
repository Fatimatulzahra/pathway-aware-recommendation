import csv
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
REVIEW = ROOT / "results" / "review" / "relevance_review.csv"


def dcg(ratings):
    return sum(
        (2 ** rating - 1) / math.log2(rank + 2)
        for rank, rating in enumerate(ratings)
    )


def main():
    judgments = {}

    with REVIEW.open(encoding="utf-8-sig", newline="") as file:
        for row_number, row in enumerate(csv.DictReader(file), start=2):
            key = (row["profile_id"], row["opportunity_id"])
            value = row["rating"].strip()

            if value not in {"0", "1", "2"}:
                raise ValueError(
                    f"Row {row_number}: rating must be 0, 1, or 2."
                )

            if key in judgments:
                raise ValueError(f"Duplicate judgment: {key}")

            judgments[key] = int(value)

    rankings = pd.read_csv(
        TABLES / "recommendation_rankings.csv",
        keep_default_na=False,
    )
    runs = pd.read_csv(TABLES / "comparison_runs.csv")
    runs = runs[runs["k"] == 5]

    if runs.duplicated(["profile_id", "method", "k"]).any():
        raise ValueError("Duplicate comparison runs.")

    top_five = rankings[rankings["k"] == 5]
    expected_pairs = set(zip(
        top_five["profile_id"],
        top_five["opportunity_id"],
    ))

    if set(judgments) != expected_pairs:
        missing = expected_pairs - set(judgments)
        extra = set(judgments) - expected_pairs
        raise ValueError(
            f"Review does not match rankings."
            f"\nMissing pairs: {sorted(missing)}"
            f"\nExtra pairs: {sorted(extra)}"
        )

    rows = []

    for run in runs.to_dict("records"):
        profile_id = run["profile_id"]
        selected = top_five[
            (top_five["profile_id"] == profile_id)
            & (top_five["method"] == run["method"])
        ].sort_values("rank")

        ids = selected["opportunity_id"].tolist()

        if len(ids) != run["returned_count"]:
            raise ValueError("Returned count does not match rankings.")

        if len(ids) > 5 or len(set(ids)) != len(ids):
            raise ValueError("Invalid top-five recommendation list.")

        if selected["rank"].tolist() != list(range(1, len(ids) + 1)):
            raise ValueError("Ranks must be consecutive starting at 1.")

        ratings = [
            judgments[(profile_id, opportunity_id)]
            for opportunity_id in ids
        ]

        pool_ratings = [
            rating
            for (student_id, _), rating in judgments.items()
            if student_id == profile_id
        ]
        ideal = sorted(pool_ratings, reverse=True)[:5]
        ideal_dcg = dcg(ideal)

        rows.append({
            "profile_id": profile_id,
            "method": run["method"],
            "k": 5,
            "returned_count": len(ids),
            "directly_relevant_count": sum(r == 2 for r in ratings),
            "precision_at_5": sum(r == 2 for r in ratings) / 5,
            "pooled_ndcg_at_5": (
                dcg(ratings) / ideal_dcg if ideal_dcg else 0.0
            ),
        })

    metrics = pd.DataFrame(rows)
    metrics.to_csv(
        TABLES / "relevance_metrics_by_profile.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary = metrics.groupby("method", as_index=False).agg(
        profiles=("profile_id", "count"),
        precision_at_5=("precision_at_5", "mean"),
        pooled_ndcg_at_5=("pooled_ndcg_at_5", "mean"),
    )
    summary.to_csv(
        TABLES / "relevance_metrics_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nPRELIMINARY RELEVANCE COMPARISON")
    print(summary.round(3).to_string(index=False))
    print("\nPrecision counts only rating 2 as relevant.")
    print("nDCG uses graded gains: 0, 1, and 3.")
    print("Ideal rankings use each profile's reviewed pool.")
    print("Zero ideal gain is assigned nDCG = 0.")
    print("Judgments assess interest match using seed descriptions.")
    print("\nSaved relevance metrics to results/tables.")


if __name__ == "__main__":
    main()