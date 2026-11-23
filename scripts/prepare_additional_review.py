import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results/tables"
REVIEW = ROOT / "results/review"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main():
    opportunities = json.loads(
        (ROOT / "data/processed/opportunities_clean.json")
        .read_text(encoding="utf-8")
    )
    profiles = json.loads(
        (ROOT / "data/profiles/student_profiles.json")
        .read_text(encoding="utf-8")
    )

    opportunity_lookup = {o["id"]: o for o in opportunities}
    profile_lookup = {p["id"]: p for p in profiles}

    existing = read_csv(REVIEW / "relevance_review.csv")
    judged = set()

    for row in existing:
        if row["rating"].strip() not in {"0", "1", "2"}:
            raise ValueError("An existing relevance rating is incomplete.")
        key = (row["profile_id"], row["opportunity_id"])
        if key in judged:
            raise ValueError(f"Duplicate existing judgment: {key}")
        judged.add(key)

    rankings = read_csv(
        TABLES / "recommendation_rankings_all_methods.csv"
    )
    required = {
        (row["profile_id"], row["opportunity_id"])
        for row in rankings
        if int(row["k"]) == 5
    }
    new_pairs = sorted(required - judged)

    rows = []
    for profile_id, opportunity_id in new_pairs:
        profile = profile_lookup[profile_id]
        opportunity = opportunity_lookup[opportunity_id]

        rows.append({
            "profile_id": profile_id,
            "profile_interests": profile["query"],
            "opportunity_id": opportunity_id,
            "title": opportunity["title"],
            "organization": opportunity["org"],
            "description": opportunity["description"],
            "requirements": opportunity["requirements"],
            "rating": "",
            "review_notes": "",
        })

    random.Random(42).shuffle(rows)
    REVIEW.mkdir(parents=True, exist_ok=True)
    output = REVIEW / "relevance_review_additional.csv"

    with output.open("x", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "profile_id", "profile_interests", "opportunity_id",
            "title", "organization", "description", "requirements",
            "rating", "review_notes",
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Unique top-five pairs across all methods: {len(required)}")
    print(f"Previously rated pairs reused: {len(required & judged)}")
    print(f"Additional pairs to rate: {len(rows)}")
    print(f"Saved to: {output}")
    print("Reuse earlier ratings only if their source descriptions")
    print("and profile interests have not changed.")


if __name__ == "__main__":
    main()