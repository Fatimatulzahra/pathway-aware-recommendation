# Career Pathway Taxonomy (Final — 12 pathways)

This document defines the twelve CS career pathways used as the **ground-truth
labeling scheme** for the opportunity corpus. Consistent definitions matter:
the labels are what every relevance, diversity, and coverage metric is scored
against, so an opportunity must be labeled the same way every time regardless of
who (or when) it is labeled.

## How to label (rules)

1. **Multi-label is expected.** Most opportunities touch 1–3 pathways. Tag every
   pathway that is a *substantial* part of the role, not every pathway it
   remotely mentions.
2. **Label the work, not the employer.** A data-analyst role at a bank is
   `data_science`, not `quant_finance`, unless the work itself is markets/trading.
3. **`research_grad_school` is about the *nature* of the work** (produces new
   knowledge, mentored by faculty/researchers, aims at a paper/poster or grad
   school), and it usually co-occurs with a *domain* pathway (e.g. an ML REU is
   `research_grad_school` + `machine_learning_ai`).
4. **When torn between two, keep both** rather than guessing — the diversity
   metric depends on honest multi-labeling.
5. **Cap at 3 labels** in normal cases. If you want a 4th, re-read rule 1.

---

## The pathways

**`software_engineering` — Software Engineering**
Designing, building, testing, and shipping general-purpose software: web/backend/
mobile/full-stack app development, APIs, systems programming. The default
"build product features" track. Signals: SWE intern, full-stack, backend, mobile.

**`data_science` — Data Science / Analytics**
Turning data into insight: analysis, statistics, visualization, dashboards,
experimentation, business/decision analytics. Python/R/SQL, pandas, notebooks.
Distinct from ML in that the deliverable is *understanding/insight*, not a
trained predictive model in production. Signals: data analyst, BI, analytics.

**`machine_learning_ai` — Machine Learning / AI**
Building models that learn or reason: ML/DL, NLP, computer vision, LLMs,
recommender systems, MLOps. The deliverable is a *model* or AI system. Signals:
ML engineer, AI research, applied scientist, deep learning.

**`cybersecurity` — Cybersecurity**
Protecting systems and data: security engineering, penetration testing, threat
detection, incident response, cryptography, secure software, digital forensics.
Signals: security analyst/engineer, red team, SOC, appsec, CTF.

**`research_grad_school` — Research / Grad School**
Producing new knowledge under faculty/lab mentorship, oriented toward a paper,
poster, publication, or graduate study. Includes REUs and university lab
programs. Almost always paired with a domain pathway. Signals: REU, research
assistant, lab, PhD prep, publication.

**`hardware_embedded` — Hardware / Embedded Systems**
Working close to physical devices and silicon: embedded firmware,
microcontrollers, FPGAs, chip/ASIC design, robotics, IoT, computer architecture.
Signals: embedded, firmware, VLSI, FPGA, RTL, hardware, robotics.

**`devops_cloud` — DevOps / Cloud / Infrastructure**
Keeping software running and shippable at scale: CI/CD, containers/Kubernetes,
cloud (AWS/GCP/Azure), SRE, infrastructure, platform, networking. Signals: SRE,
platform, infrastructure, cloud, DevOps, reliability.

**`product_management` — Product Management**
Deciding *what* to build and why: product strategy, requirements, roadmaps,
working across engineering/design/business. Technical PM / APM tracks. Signals:
product manager, APM, product intern.

**`ux_design` — UX / Human-Computer Interaction**
How people experience software: UX/UI design, interaction design, user research,
usability, accessibility, HCI research. Signals: UX, product design, design
research, HCI, usability.

**`quant_finance` — Quant / Fintech**
Computing applied to markets and money: quantitative research/trading,
algorithmic trading, risk modeling, fintech engineering. Signals: quant,
trading, markets, hedge fund, fintech.

**`game_development` — Game Development**
Building games and interactive/real-time media: game engines, graphics, gameplay
programming, XR/AR/VR. Signals: game dev, Unity/Unreal, graphics, gameplay, XR.

**`civic_tech` — Civic / Public-Interest Tech**
Technology for government, nonprofits, and public good: civic tech, govtech,
public-interest software, tech for social impact. Signals: civic, government,
nonprofit, public interest, social good, policy.
