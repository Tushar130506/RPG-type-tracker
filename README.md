📘 life_rpg — Personal Life RPG Engine (WIP)

A fully local, privacy-first life simulation engine that models your real habits, tasks, journaling, and trends as an RPG progression system.

This project turns daily actions into XP, updates long-term stats, detects patterns, and generates realistic weekly & monthly reports — without motivational fluff or inflated numbers.

🚀 Core Systems Implemented
🧠 Daily Pipeline (complete skeleton)

Ingest daily logs

Segment raw text into atomic events

Match events (task, finance, mental, lifestyle)

Run placeholder agents

Compute XP

Apply anti-spam + diminishing returns

Apply streak logic + consistency multipliers

Apply daily & weekly XP caps

Save daily snapshots (placeholder)

📝 Segmentation Engine (v1)

Deterministic rule-based segmentation:

Cleans noisy text

Splits events using linguistic cues

Merges small fragments

Produces clean, atomic actions

🎯 Event Matching Engine (v1)

Maps segmented text into:

task_event (strength / intelligence / lifestyle)

mental_event

finance_event

ignore_event

Keyword-based for now — upgradeable to LLM later.

⚔ XP Engine (v1)

Real RPG-style XP system:

Effort scoring

Difficulty multipliers

Streak & consistency multipliers

Repetition-based diminishing returns

Per-event XP

Per-stat XP aggregation

🔥 Anti-Spam Mechanics

Diminishing returns on repeated tasks

Category repetition counters per day

📈 Streak System

Per-category streak counters

Last-active-day tracking

Consistency multipliers: 1.0 → 1.2 → 1.35 → 1.5

Reset on inactivity

🛡 XP Caps (balanced progression)

Soft cap after 18 XP (extra × 0.6)

Hard cap at 25 XP/day/stat

Weekly soft caps (XP > weekly_avg × 1.8 → −30%)



📅 Roadmap
Next Up

SQLite integration (daily logs, snapshots, XP events)

Persistent streak + XP history

Mental health analysis v1

Finance event analysis v1

Anti-farming engine v2

Weekly & monthly report generator

Planned + optional task system

FastAPI backend

Local UI / desktop app

Future

LLM-based segmentation

Smart classification agent

Natural language reporting

Visualization dashboard

Local vector search for patterns

💡 Philosophy

This is not a habit tracker.
This is not a dopamine app.

This is a life telemetry engine, designed like a strategy game:

No toxic positivity

No inflated XP

No judgment

No spam rewards

No shortcuts

Consistency > intensity.
Patterns > feelings.
Data > motivation.

🛠 Tech Stack

Python 3.11

SQLite (local persistence)

SQLAlchemy (ORM)

FastAPI (future API)

Local desktop UI (later)

🧪 Running the pipeline (dev mode)
python test_pipeline.py

🔒 Privacy

Everything runs locally only.
No cloud, no analytics, no external calls.
