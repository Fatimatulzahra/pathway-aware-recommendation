# pathway-aware-recommendation
# Pathway-Aware Opportunity Recommendation

### Broadening Computer Science Career Exploration Through Pathway-Aware Recommendations

## Overview

Computer science students can encounter a narrow view of what careers in computing can look like. Software engineering is often one of the most visible pathways, while areas such as data science, machine learning, cybersecurity, research, graduate study, and hardware development may receive less exposure.

This project investigates whether a **pathway-aware recommendation approach** can broaden the range of opportunities presented to computer science students without substantially reducing recommendation relevance.

Rather than relying primarily on keyword overlap, recency, or popularity, the project explicitly considers the career pathway associated with each opportunity and the pathway interests of a student.

The project is designed as a comparative research study using the same opportunity corpus, student profiles, and evaluation criteria across multiple recommendation approaches.

## Research Question

> **Can pathway-aware recommendation improve the diversity and pathway coverage of recommended opportunities without substantially reducing relevance, and how do different recommendation approaches compare on this tradeoff?**

## Project Goals

This project aims to:

- Build a labeled corpus of computer science opportunities.
- Define a consistent taxonomy of career pathways.
- Create representative student profiles based on pathway interests and academic year.
- Implement three different recommendation approaches.
- Compare the approaches using quantitative evaluation metrics.
- Analyze the tradeoff between relevance, diversity, and pathway coverage.
- Develop a reproducible evaluation pipeline for studying recommendation systems.

## Recommendation Approaches

The study will compare three recommendation methods.

### 1. Keyword + Recency Baseline

The baseline method represents a conventional recommendation approach using:

- Keyword matching
- Student interests
- Opportunity text
- Opportunity recency

This provides a reference point for comparing the more pathway-aware approaches.

### 2. Content-Based Recommendation

The content-based recommender will use:

- TF-IDF representations
- Opportunity descriptions
- Pathway information
- Cosine similarity

Opportunities will be ranked according to their similarity to a student's profile and interests.

### 3. LLM-Assisted Recommendation

The LLM-assisted approach will use a large language model to:

1. Classify opportunities into career pathways.
2. Interpret the student's pathway interests.
3. Rank opportunities for the given student profile.

The results will then be evaluated using the same criteria as the other recommendation methods.

## Career Pathway Taxonomy

Each opportunity will be manually labeled according to a fixed taxonomy of approximately 10–12 computer science career pathways.

Potential pathways include areas such as:

- Software Engineering
- Data Science
- Machine Learning / AI
- Cybersecurity
- Research
- Graduate Study
- Hardware / Computer Architecture
- UI/UX / Human-Computer Interaction
- Web Development
- Information Technology
- Other Computing Pathways

The final taxonomy will be defined before evaluation and applied consistently across the opportunity corpus.

## Dataset

The project will use a corpus of approximately:

- **150–250 real computer science opportunities**
- **10–15 representative student profiles**

The opportunity dataset will include opportunities such as:

- Internships
- Research Experiences for Undergraduates (REUs)
- Fellowships
- Scholarships

Each opportunity will be labeled according to the defined career pathway taxonomy.

Student profiles will specify characteristics such as:

- Career pathway interests
- Academic year
- Other information necessary to establish recommendation relevance

## Evaluation

Each recommendation method will be evaluated at:

- **k = 5**
- **k = 10**
- **k = 20**

Three categories of metrics will be used.

### Relevance

Recommendation relevance will be measured using:

- Precision@k
- Recall@k
- NDCG@k

These metrics will be calculated against the hand-labeled ground truth.

### Diversity

Intra-list diversity will be used to measure how different the recommended opportunities are from one another.

The project will calculate diversity as:

> **1 − mean pairwise cosine similarity**

A higher value indicates that the recommendations are less similar to each other.

### Pathway Coverage

Pathway coverage will measure:

- The number of distinct career pathways represented within a recommendation list.
- The number of pathways represented across the full set of recommendations.
- Coverage relative to the defined pathway taxonomy.

These measures help determine whether a recommendation method exposes students to opportunities across multiple computing pathways rather than repeatedly recommending opportunities from the same area.

## Why These Metrics Matter

A recommendation system can achieve high relevance while still repeatedly recommending opportunities within a student's existing area of interest.

For this project, relevance alone is therefore not sufficient.

The evaluation considers:

**Relevance + Diversity + Pathway Coverage**

This allows the project to examine whether recommendation methods can broaden career exploration while still providing opportunities that are relevant to the student's interests.

## Existing Full-Stack Platform

This research builds on an existing full-stack opportunity platform developed during Junior Seminar using:

- React
- Node.js / Express
- MongoDB

The existing platform provides the opportunity-listing interface and pathway concept.

The platform may be used for an optional demonstration of the recommendation system.

However, the primary research evaluation will be conducted separately as an **offline Python pipeline** using:

- Python
- scikit-learn
- NumPy
- pandas

This separation allows the recommendation methods to be evaluated consistently using the same dataset, student profiles, and metrics.

## Project Workflow

The planned research workflow is:

```text
Collect Opportunities
        ↓
Clean & Preprocess Data
        ↓
Define Career Pathway Taxonomy
        ↓
Manually Label Opportunities
        ↓
Create Student Profiles
        ↓
        ┌─────────────────────┐
        │ Same Dataset/Profile│
        └──────────┬──────────┘
                   ↓
     ┌─────────────┼─────────────┐
     ↓             ↓             ↓
Keyword +      TF-IDF +       LLM-Assisted
Recency        Content-Based   Recommendation
     ↓             ↓             ↓
     └─────────────┼─────────────┘
                   ↓
             Evaluate @ k
             5, 10, 20
                   ↓
       ┌───────────┼───────────┐
       ↓           ↓           ↓
   Relevance   Diversity   Pathway
                            Coverage
       └───────────┼───────────┘
                   ↓
          Compare Results
                   ↓
        Tables + Visualizations
                   ↓
          Research Analysis
```

## Repository Structure

```text
pathway-aware-recommendation/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── profiles/
│
├── notebooks/
│
├── src/
│   ├── data/
│   ├── recommenders/
│   ├── evaluation/
│   └── utils/
│
├── results/
│   ├── tables/
│   └── figures/
│
├── taxonomy/
│
├── docs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Technology Stack

### Research / Evaluation

- Python
- pandas
- NumPy
- scikit-learn
- Jupyter Notebook

### Recommendation

- Keyword matching
- TF-IDF
- Cosine similarity
- LLM-assisted classification and ranking

### Existing Platform

- React
- Node.js
- Express
- MongoDB

## Expected Deliverables

The final project will produce:

1. A labeled opportunity corpus.
2. A defined career pathway taxonomy.
3. Three implemented recommendation methods.
4. A set of representative student profiles.
5. A reproducible evaluation pipeline.
6. Quantitative evaluation results.
7. Tables and visualizations comparing the recommendation methods.
8. A written research report discussing the results and their implications for pathway-aware career exploration.

## Scope

This project focuses on evaluating recommendation approaches using an offline research pipeline.

A user study measuring whether students actually change their career exploration behavior is outside the scope of this semester's project and is considered a possible future extension.

## Future Work

Potential future extensions include:

- Conducting a user study with computer science students.
- Integrating the evaluated recommender into the existing opportunity platform.
- Expanding the opportunity corpus.
- Supporting additional career pathways.
- Studying how recommendations change over time as student interests evolve.

## Author

**Fatimah Badmos**

Computer Science  
Fisk University

---

## Status

**Research Project — Senior Seminar**

The project is currently in development. The repository will be updated as the dataset, recommendation methods, evaluation pipeline, and results are developed.
