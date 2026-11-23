import csv
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results/tables"
REVIEW = ROOT / "results/review"


def dcg(ratings):
    return sum(
        (2 ** rating - 1) / math.log2(rank + 2)
        for rank, rating in enumerate(ratings)
    )


def main():
    judgments = {}
    duplicate_count = 0

    for filename in [
        "relevance_review.csv",
        "relevance_review_additional.csv",
    ]:
        with (REVIEW / filename).open(
            encoding="utf-8-sig", newline=""
        ) as file:
            for number, row in enumerate(csv.DictReader(file), start=2):
                key = (row["profile_id"], row["opportunity_id"])
                value = row["rating"].strip()

                if value not in {"0", "1", "2"}:
                    raise ValueError(
                        f"{filename}, row {number}: invalid or missing rating."
                    )

                rating = int(value)

                if key in judgments:
                    if judgments[key] != rating:
                        raise ValueError(
                            f"Conflicting ratings for {key}: "
                            f"{judgments[key]} and {rating}."
                        )
                    duplicate_count += 1

                judgments[key] = rating

    rankings = pd.read_csv(
        TABLES / "recommendation_rankings_all_methods.csv",
        keep_default_na=False,
    )
    runs = pd.read_csv(TABLES / "comparison_runs_all_methods.csv")
    top_five = rankings[rankings["k"] == 5]
    runs = runs[runs["k"] == 5]

    if runs.duplicated(["profile_id", "method", "k"]).any():
        raise ValueError("Duplicate comparison runs.")

    required = set(zip(
        top_five["profile_id"],
        top_five["opportunity_id"],
    ))

    missing = required - set(judgments)
    if missing:
        raise ValueError(f"Missing ratings: {sorted(missing)}")

    # Use the same top-five candidate pool for every method.
    pool = {key: judgments[key] for key in required}
    rows = []

    for run in runs.to_dict("records"):
        profile_id = run["profile_id"]
        selected = top_five[
            (top_five["profile_id"] == profile_id)
            & (top_five["method"] == run["method"])
        ].sort_values("rank")

        ids = selected["opportunity_id"].tolist()

        if len(ids) != run["returned_count"]:
            raise ValueError("Returned count does not match ranking rows.")

        if len(ids) > 5 or len(set(ids)) != len(ids):
            raise ValueError("Invalid top-five list.")

        if selected["rank"].tolist() != list(range(1, len(ids) + 1)):
            raise ValueError("Ranks must be consecutive starting at 1.")

        ratings = [pool[(profile_id, oid)] for oid in ids]
        ideal = sorted(
            [
                rating
                for (pid, _), rating in pool.items()
                if pid == profile_id
            ],
            reverse=True,
        )[:5]

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
    counts = metrics.groupby("method")["profile_id"].nunique()

    if set(counts.index) != {"keyword", "tfidf", "llm_manual"}:
        raise ValueError("Expected all three methods.")

    expected_profiles = set(runs["profile_id"])
    for method, group in metrics.groupby("method"):
        if set(group["profile_id"]) != expected_profiles:
            raise ValueError(f"{method}: missing profiles.")

    summary = metrics.groupby("method", as_index=False).agg(
        profiles=("profile_id", "count"),
        precision_at_5=("precision_at_5", "mean"),
        pooled_ndcg_at_5=("pooled_ndcg_at_5", "mean"),
    )

    metrics.to_csv(
        TABLES / "relevance_metrics_by_profile_all_methods.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary.to_csv(
        TABLES / "relevance_metrics_summary_all_methods.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(f"\nUnique judged pairs used: {len(pool)}")
    print(f"Identical duplicate judgments merged: {duplicate_count}")
    print("\nTHREE-METHOD RELEVANCE COMPARISON")
    print(summary.round(3).to_string(index=False))
    print("\nPrecision: rating 2 counts as relevant.")
    print("Pooled nDCG: shared three-method judgment pool; gains 0, 1, 3.")
    print("Results saved to results/tables.")


if __name__ == "__main__":
    main()