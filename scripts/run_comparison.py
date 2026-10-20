import csv
import json
from pathlib import Path

from recommend import OpportunityRecommender, load_opportunities

ROOT = Path(__file__).resolve().parents[1]
PROFILE_FILE = ROOT / "data" / "profiles" / "student_profiles.json"
OUTPUT_DIR = ROOT / "results" / "tables"


def main():
    profiles = json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
    recommender = OpportunityRecommender(load_opportunities())

    ranking_rows = []
    run_rows = []

    for profile in profiles:
        for method in ["keyword", "tfidf"]:
            # Rank once, then take prefixes for each requested list size.
            ranked = recommender.recommend(
                profile["query"], method=method, k=20
            )

            for k in [5, 10, 20]:
                results = ranked[:k]

                run_rows.append({
                    "profile_id": profile["id"],
                    "profile_name": profile["name"],
                    "method": method,
                    "k": k,
                    "returned_count": len(results),
                })

                for rank, result in enumerate(results, start=1):
                    ranking_rows.append({
                        "profile_id": profile["id"],
                        "profile_name": profile["name"],
                        "query": profile["query"],
                        "target_pathways": "|".join(
                            profile["target_pathways"]
                        ),
                        "method": method,
                        "k": k,
                        "rank": rank,
                        "opportunity_id": result["id"],
                        "title": result["title"],
                        "organization": result["org"],
                        "score": result["score"],
                        "matched_terms": "|".join(
                            result["matched_terms"]
                        ),
                        "opportunity_pathways": "|".join(
                            result["pathways"]
                        ),
                        "verified": result["verified"],
                        "link": result["link"],
                    })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ranking_fields = [
        "profile_id", "profile_name", "query", "target_pathways",
        "method", "k", "rank", "opportunity_id", "title",
        "organization", "score", "matched_terms",
        "opportunity_pathways", "verified", "link",
    ]
    run_fields = [
        "profile_id", "profile_name", "method", "k",
        "returned_count",
    ]

    for filename, rows, fields in [
        ("recommendation_rankings.csv", ranking_rows, ranking_fields),
        ("comparison_runs.csv", run_rows, run_fields),
    ]:
        path = OUTPUT_DIR / filename
        with path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    print(f"Profiles evaluated: {len(profiles)}")
    print(f"Comparison runs: {len(run_rows)}")
    print(f"Ranking rows saved: {len(ranking_rows)}")

    short_lists = sum(
        row["returned_count"] < row["k"]
        for row in run_rows
    )
    print(f"Runs returning fewer than k matches: {short_lists}")
    print(f"Results saved in: {OUTPUT_DIR}")
    print("Preliminary results: seed opportunity labels are unverified.")


if __name__ == "__main__":
    main()