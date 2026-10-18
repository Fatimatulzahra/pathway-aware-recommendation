import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "opportunities.json"
OUTPUT = ROOT / "data" / "processed" / "opportunities_clean.json"

TEXT_FIELDS = [
    "title", "org", "type", "description", "requirements", "link"
]


def main():
    with SOURCE.open(encoding="utf-8") as file:
        opportunities = json.load(file)

    cleaned = []

    for opportunity in opportunities:
        record = opportunity.copy()

        # Remove accidental leading/trailing whitespace.
        for field in TEXT_FIELDS:
            record[field] = record[field].strip()

        # Remove repeated labels while preserving their order.
        record["pathways"] = list(dict.fromkeys(record["pathways"]))

        # The seed dates are placeholders, not observed posting dates.
        record["date_posted"] = None
        record["date_posted_status"] = "unknown"

        # Existing pathway labels have not yet been manually reviewed.
        record["label_review_status"] = "pending"

        cleaned.append(record)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Prevent accidentally overwriting later manual corrections.
    with OUTPUT.open("x", encoding="utf-8") as file:
        json.dump(cleaned, file, indent=2, ensure_ascii=False)
        file.write("\n")

    print(f"Saved {len(cleaned)} records to {OUTPUT}")
    print("Original dataset unchanged.")
    print("Placeholder posting dates replaced with null.")
    print("Pathway labels preserved and marked pending review.")


if __name__ == "__main__":
    main()