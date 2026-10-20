import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "review" / "relevance_review.csv"


def main():
    profiles = json.loads(
        (ROOT / "data/profiles/student_profiles.json")
        .read_text(encoding="utf-8")
    )
    opportunities = json.loads(
        (ROOT / "data/processed/opportunities_clean.json")
        .read_text(encoding="utf-8")
    )

    profile_lookup = {p["id"]: p for p in profiles}
    opportunity_lookup = {o["id"]: o for o in opportunities}

    rankings_path = ROOT / "results/tables/recommendation_rankings.csv"
    with rankings_path.open(encoding="utf-8-sig", newline="") as file:
        rankings = list(csv.DictReader(file))

    # Pool both methods' top-five results.
    # Review an opportunity only once for each profile.
    pairs = sorted({
        (row["profile_id"], row["opportunity_id"])
        for row in rankings
        if int(row["k"]) == 5
    })

    rows = []
    for profile_id, opportunity_id in pairs:
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

    # Fixed seed makes the shuffled review order reproducible.
    random.Random(42).shuffle(rows)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Avoid overwriting ratings if this script is run again.
    with OUTPUT.open("x", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "profile_id", "profile_interests", "opportunity_id",
                "title", "organization", "description", "requirements",
                "rating", "review_notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {len(rows)} profile–opportunity review pairs.")
    print(f"Saved to: {OUTPUT}")
    print("Enter ratings in the rating column; leave IDs unchanged.")


if __name__ == "__main__":
    main()