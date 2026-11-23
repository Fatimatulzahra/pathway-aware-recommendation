import csv
import hashlib
import json
from pathlib import Path

from recommend import tokenize

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results/tables"
LLM = ROOT / "results/llm_manual"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames, list(reader)


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    opportunities = read_json(
        ROOT / "data/processed/opportunities_clean.json"
    )
    profiles = read_json(
        ROOT / "data/profiles/student_profiles.json"
    )
    lookup = {record["id"]: record for record in opportunities}

    # Confirm the opportunity text still matches the prompt-generation corpus.
    candidates = [
        {
            "id": record["id"],
            "title": record["title"],
            "description": record["description"],
            "requirements": record["requirements"],
        }
        for record in opportunities
    ]
    corpus = json.dumps(candidates, ensure_ascii=False, indent=2)
    current_hash = hashlib.sha256(corpus.encode("utf-8")).hexdigest()
    manifest = read_json(LLM / "manifest.json")

    if current_hash != manifest["corpus_sha256"]:
        raise ValueError(
            "Dataset text changed after prompts were generated. "
            "Stop and check which dataset was used."
        )

    ranking_fields, ranking_rows = read_csv(
        TABLES / "recommendation_rankings.csv"
    )
    run_fields, run_rows = read_csv(
        TABLES / "comparison_runs.csv"
    )

    if {row["method"] for row in run_rows} != {"keyword", "tfidf"}:
        raise ValueError("Expected the original two-method comparison files.")

    ranking_fields = list(ranking_fields)
    if "reason" not in ranking_fields:
        ranking_fields.append("reason")

    counts = []

    for profile in profiles:
        path = LLM / "responses" / f'{profile["id"]}.json'
        response = read_json(path)

        if response.get("profile_id") != profile["id"]:
            raise ValueError(f"{path.name}: wrong profile_id.")

        recommendations = response.get("recommendations")
        if not isinstance(recommendations, list):
            raise ValueError(f"{path.name}: recommendations must be a list.")

        if len(recommendations) > 20:
            raise ValueError(f"{path.name}: more than 20 recommendations.")

        seen = set()

        for item in recommendations:
            opportunity_id = item.get("opportunity_id")

            if opportunity_id not in lookup:
                raise ValueError(
                    f"{path.name}: unknown ID {opportunity_id}."
                )
            if opportunity_id in seen:
                raise ValueError(
                    f"{path.name}: duplicate ID {opportunity_id}."
                )
            if not isinstance(item.get("reason"), str) or not item["reason"].strip():
                raise ValueError(
                    f"{path.name}: missing reason for {opportunity_id}."
                )

            seen.add(opportunity_id)

        counts.append((profile["id"], len(recommendations)))

        for k in [5, 10, 20]:
            selected = recommendations[:k]

            run_rows.append({
                "profile_id": profile["id"],
                "profile_name": profile["name"],
                "method": "llm_manual",
                "k": k,
                "returned_count": len(selected),
            })

            for rank, item in enumerate(selected, start=1):
                opportunity = lookup[item["opportunity_id"]]

                ranking_rows.append({
                    "profile_id": profile["id"],
                    "profile_name": profile["name"],
                    "query": profile["query"],
                    "target_pathways": "|".join(
                        profile["target_pathways"]
                    ),
                    "method": "llm_manual",
                    "k": k,
                    "rank": rank,
                    "opportunity_id": opportunity["id"],
                    "title": opportunity["title"],
                    "organization": opportunity["org"],
                    # The model returned an order, not numerical scores.
                    "score": "",
                    "matched_terms": "",
                    "opportunity_pathways": "|".join(
                        opportunity["pathways"]
                    ),
                    "verified": opportunity.get("verified", False),
                    "link": opportunity.get("link", ""),
                    "reason": item["reason"],
                })

    # Check that every profile/method/list-size combination occurs once.
    expected = {
        (profile["id"], method, k)
        for profile in profiles
        for method in ["keyword", "tfidf", "llm_manual"]
        for k in [5, 10, 20]
    }
    actual = [
        (row["profile_id"], row["method"], int(row["k"]))
        for row in run_rows
    ]

    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError("Missing or duplicate comparison runs.")

    write_csv(
        TABLES / "recommendation_rankings_all_methods.csv",
        ranking_fields,
        ranking_rows,
    )
    write_csv(
        TABLES / "comparison_runs_all_methods.csv",
        run_fields,
        run_rows,
    )

    print("\nLLM RESPONSE VALIDATION")
    for profile_id, count in counts:
        print(f"{profile_id}: {count} valid recommendations")

    print(f"\nTotal comparison runs: {len(run_rows)}")
    print("Saved combined rankings and runs to results/tables.")
    print("Original responses and two-method results unchanged.")
    print("Validation checks format and IDs, not ranking quality.")


if __name__ == "__main__":
    main()