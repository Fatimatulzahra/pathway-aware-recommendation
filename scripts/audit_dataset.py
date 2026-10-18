import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "opportunities.json"
TAXONOMY_FILE = ROOT / "data" / "taxonomy.py"

# Load the taxonomy without requiring a Python package setup.
import runpy

PATHWAYS = runpy.run_path(str(TAXONOMY_FILE))["PATHWAYS"]


def main():
    with DATA_FILE.open(encoding="utf-8") as file:
        opportunities = json.load(file)

    total = len(opportunities)
    pathway_counts = Counter()
    type_counts = Counter()
    id_counts = Counter()
    title_org_counts = Counter()
    issues = []

    required_fields = [
        "id", "title", "org", "type",
        "description", "requirements", "link", "pathways",
    ]

    for index, opportunity in enumerate(opportunities, start=1):
        label = opportunity.get("id") or f"record {index}"

        for field in required_fields:
            if not opportunity.get(field):
                issues.append(f"{label}: missing or empty {field}")

        id_counts[opportunity.get("id")] += 1
        title_org_counts[
            (
                opportunity.get("title", "").strip().casefold(),
                opportunity.get("org", "").strip().casefold(),
            )
        ] += 1
        type_counts[opportunity.get("type", "missing")] += 1

        pathways = opportunity.get("pathways", [])
        if not isinstance(pathways, list):
            issues.append(f"{label}: pathways must be a list")
            continue

        if len(pathways) != len(set(pathways)):
            issues.append(f"{label}: repeated pathway labels")

        for pathway in set(pathways):
            if pathway not in PATHWAYS:
                issues.append(f"{label}: unknown pathway {pathway}")
            else:
                pathway_counts[pathway] += 1

    print(f"\nTOTAL OPPORTUNITIES: {total}")

    verified = sum(
        opportunity.get("verified") is True
        for opportunity in opportunities
    )
    print(f"Verified: {verified}/{total}")

    print("\nPATHWAY COVERAGE")
    print(f"{'Pathway':<38} {'Count':>6} {'% of records':>14}")
    for pathway, name in PATHWAYS.items():
        count = pathway_counts[pathway]
        percentage = 100 * count / total if total else 0
        print(f"{name:<38} {count:>6} {percentage:>13.1f}%")

    print("\nCounts overlap because opportunities can have multiple labels.")

    print("\nOPPORTUNITY TYPES")
    for opportunity_type, count in type_counts.most_common():
        print(f"  {opportunity_type}: {count}")

    print("\nDUPLICATE IDS")
    duplicates = {key: count for key, count in id_counts.items() if count > 1}
    print(duplicates or "None")

    print("\nDUPLICATE TITLE + ORGANIZATION")
    duplicates = {
        key: count for key, count in title_org_counts.items() if count > 1
    }
    print(duplicates or "None")

    print("\nFIELD AND LABEL ISSUES")
    if issues:
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("None")

    print(
        "\nNOTE: The seed build script identifies posting dates as placeholders."
        "\nThis audit does not verify program availability, links, or label accuracy."
    )


if __name__ == "__main__":
    main()