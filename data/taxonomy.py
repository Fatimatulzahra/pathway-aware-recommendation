"""
The pathway taxonomy: the fixed set of CS career pathways (FINAL, 12 pathways).

This is the SPINE of the whole project. Every opportunity in the corpus is
labeled with one or more of these ids, every student profile expresses interest
in one or more of these, and the "pathway coverage" metric is measured relative
to this list. It is now frozen -- changing it means relabeling the corpus.

Machine-readable ids are snake_case and stable. Display names are for tables
and figures only. Full prose definitions live in docs/pathway_taxonomy.md.
"""

# id -> human-readable label
PATHWAYS = {
    "software_engineering": "Software Engineering",
    "data_science":         "Data Science / Analytics",
    "machine_learning_ai":  "Machine Learning / AI",
    "cybersecurity":        "Cybersecurity",
    "research_grad_school": "Research / Grad School",
    "hardware_embedded":    "Hardware / Embedded Systems",
    "devops_cloud":         "DevOps / Cloud / Infrastructure",
    "product_management":   "Product Management",
    "ux_design":            "UX / Human-Computer Interaction",
    "quant_finance":        "Quant / Fintech",
    "game_development":     "Game Development",
    "civic_tech":           "Civic / Public-Interest Tech",
}

# A plain list of the ids, handy for iterating and for building vectors.
PATHWAY_IDS = list(PATHWAYS.keys())

# Total number of pathways -- the denominator for pathway-coverage metrics.
NUM_PATHWAYS = len(PATHWAY_IDS)
