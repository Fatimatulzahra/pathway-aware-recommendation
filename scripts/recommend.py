import argparse
import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import (
    ENGLISH_STOP_WORDS,
    TfidfVectorizer,
)
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "opportunities_clean.json"


def opportunity_text(opportunity):
    """Use the same information for both recommendation methods."""
    fields = ["title", "description", "requirements"]
    return " ".join(opportunity.get(field) or "" for field in fields)


def tokenize(text):
    """Keep meaningful words and terms such as C++, C#, and CI/CD."""
    tokens = re.findall(r"[a-z0-9]+(?:[+#/][a-z0-9+#]*)*", text.lower())
    return [
        token
        for token in tokens
        if token not in ENGLISH_STOP_WORDS
    ]


def load_opportunities(path=DATA_FILE):
    with path.open(encoding="utf-8") as file:
        opportunities = json.load(file)

    if not isinstance(opportunities, list) or not opportunities:
        raise ValueError("Dataset must be a nonempty list.")

    ids = [opportunity["id"] for opportunity in opportunities]
    if len(ids) != len(set(ids)):
        raise ValueError("Opportunity IDs must be unique.")

    return opportunities


class OpportunityRecommender:
    def __init__(self, opportunities):
        if not opportunities:
            raise ValueError("At least one opportunity is required.")

        self.opportunities = opportunities
        self.texts = [
            opportunity_text(opportunity)
            for opportunity in opportunities
        ]
        self.token_sets = [
            set(tokenize(text))
            for text in self.texts
        ]

        self.vectorizer = TfidfVectorizer(
            tokenizer=tokenize,
            token_pattern=None,
            lowercase=False,
            ngram_range=(1, 2),
            sublinear_tf=True,
        )

        # Learn vocabulary and IDF weights from opportunities only.
        self.matrix = self.vectorizer.fit_transform(self.texts)

    def recommend(self, query, method="tfidf", k=5):
        if k < 1:
            raise ValueError("k must be at least 1.")

        query_tokens = set(tokenize(query))
        if not query_tokens:
            raise ValueError("Enter at least one meaningful search term.")

        if method == "keyword":
            scores = [
                len(query_tokens & tokens) / len(query_tokens)
                for tokens in self.token_sets
            ]

        elif method == "tfidf":
            # Transform the query using the existing vocabulary.
            query_vector = self.vectorizer.transform([query])
            scores = cosine_similarity(
                query_vector, self.matrix
            ).ravel().tolist()

        else:
            raise ValueError(f"Unknown method: {method}")

        # Use ID to make tied rankings reproducible.
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: (
                -scores[index],
                self.opportunities[index]["id"],
            ),
        )

        results = []
        for index in ranked_indices:
            # Do not present zero-similarity records as matches.
            if scores[index] <= 0:
                continue

            opportunity = self.opportunities[index]
            results.append({
                "id": opportunity["id"],
                "title": opportunity["title"],
                "org": opportunity["org"],
                "score": float(scores[index]),
                "matched_terms": sorted(
                    query_tokens & self.token_sets[index]
                ),
                "pathways": opportunity.get("pathways", []),
                "link": opportunity.get("link", ""),
                "verified": opportunity.get("verified", False),
            })

            if len(results) == k:
                break

        return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument(
        "--method",
        choices=["keyword", "tfidf", "both"],
        default="both",
    )
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    if args.k < 1:
        parser.error("--k must be at least 1.")

    if not tokenize(args.query):
        parser.error("--query must contain meaningful search terms.")

    recommender = OpportunityRecommender(load_opportunities())
    methods = (
        ["keyword", "tfidf"]
        if args.method == "both"
        else [args.method]
    )

    print(f"\nQuery: {args.query}")
    print("Seed dataset: program details are not yet verified.")
    print("Scores from different methods are not directly comparable.")

    for method in methods:
        print(f"\n{method.upper()} — TOP {args.k}")
        results = recommender.recommend(
            args.query, method=method, k=args.k
        )

        if not results:
            print("No matching terms found. Try different wording.")
            continue

        for rank, result in enumerate(results, start=1):
            print(
                f"\n{rank}. {result['title']} | {result['org']}"
                f"\n   ID: {result['id']}"
                f"\n   Score: {result['score']:.4f}"
                f"\n   Matched terms: {', '.join(result['matched_terms'])}"
                f"\n   Pathways: {', '.join(result['pathways'])}"
                f"\n   Link: {result['link']}"
            )


if __name__ == "__main__":
    main()