# DAY 2 Progress Report
## IEEE Research Project

**Student:** Sanket Sanjay Jadhav  
**Program:** Master of Computer Applications (MCA)  
**Research Area:** Text-to-SQL using Small Open-Weight Large Language Models  
**Date:** Day 2

---

# Project Title

**Empirical Benchmarking of Small Open-Weight LLMs in Text-to-SQL: A Lightweight Schema Pruning and Execution-Feedback Approach**

---

# Day 2 Objective

The primary objective of Day 2 was to complete the **baseline research framework** before integrating any Large Language Models (LLMs). Instead of focusing on model inference, the effort was directed toward building a modular, reusable, and reproducible architecture that can support multiple prompting strategies and future research extensions.

---

# Major Architectural Decisions

During today's discussion and implementation, several important design decisions were finalized.

## 1. Modular Research Framework

The project was organized into independent components following the principle of **single responsibility**, ensuring that each module performs one well-defined task.

Current pipeline:

Spider Dataset

↓

Dataset Loader

↓

Schema Extractor

↓

Schema Formatter

↓

Prompt Builder

↓

(Model Runner – To Be Implemented)

↓

(SQL Executor – To Be Implemented)

↓

Evaluator

This modular design allows future prompting techniques and LLMs to be integrated without modifying the existing framework.

---

## 2. Prompt Templates Separated from Python Code

Instead of hardcoding prompts inside Python scripts, all prompts are stored as standalone template files.

Current prompt directory:

prompts/

- zero_shot.txt
- few_shot.txt
- cot.txt
- hybrid.txt

Benefits:

- Improved reproducibility
- Easier prompt engineering
- Cleaner source code
- Suitable for research publication

---

## 3. Standardized Project Structure

The repository was reorganized into a research-oriented structure.

```
spider_data/

├── checkpoints/
├── data/
│   ├── database/
│   ├── excluded_databases/
│   ├── dev.json
│   └── tables.json
│
├── docs/
│   ├── DAY1.md
│   └── DAY2.md
│
├── experiments/
│   ├── run_baseline.py
│   └── __init__.py
│
├── logs/
├── prompts/
├── results/
├── src/
├── tests/
├── tools/
│
├── config.py
├── README.md
├── requirements.txt
└── .gitignore
```

The architecture is now considered stable and will remain unchanged unless critical issues are discovered.

---

# Dataset Optimization

While preparing the Spider benchmark dataset, it was observed that the database directory occupied approximately **900 MB**.

Investigation revealed that two databases accounted for the majority of the storage:

- soccer_1.sqlite (~309 MB)
- wta_1.sqlite (~102 MB)

Rather than modifying the original Spider dataset, these two databases were **moved to an `excluded_databases` directory**.

Current status:

- Original Spider dataset preserved
- Research copy contains 164 databases
- Excluded databases stored separately
- Storage requirement significantly reduced for daily development

This optimization simplifies local development while keeping the excluded databases available if future experiments require them.

The exclusion will be explicitly documented in the methodology section if these databases are omitted from the final benchmark subset.

---

# Modules Completed

## Dataset Loader

Implemented:

- Load dev.json
- Load tables.json
- Return individual questions
- Dataset statistics

Current statistics:

- Questions: 1034
- Databases: 166

---

## Schema Extractor

Implemented extraction of:

- Database name
- Table names
- Column names
- Primary keys
- Foreign keys
- Metadata

Example metadata:

- Number of tables
- Number of columns
- Primary key count
- Foreign key count

---

## Schema Formatter

Implemented conversion of structured schema into LLM-readable text.

Example:

Database: concert_singer

Table: singer

- Singer_ID
- Name
- Country
- Age

Relationships

concert.Stadium_ID -> stadium.Stadium_ID

This formatted schema is now reused by all prompting strategies.

---

## Prompt Builder

Implemented a reusable PromptBuilder that loads prompt templates directly from the prompts directory.

Current implementation supports:

- Zero-Shot prompting

Future implementations:

- Few-Shot
- Chain-of-Thought
- Schema Pruning
- Hybrid Prompt

Prompt templates now use placeholders:

{schema}

{question}

instead of hardcoded values.

---

## Data Models

Introduced standardized dataclasses.

GenerationResult

Stores:

- model_name
- prompt_type
- prompt
- generated_sql
- latency
- success
- error

ExperimentResult

Stores:

- Question information
- Gold SQL
- Generated SQL
- Execution status
- Evaluation metrics

These classes will become the standard interface between the LLM, SQL executor, and evaluator.

---

# Testing and Validation

A complete integration test was implemented.

Pipeline verified:

Dataset Loader

↓

Schema Extractor

↓

Schema Formatter

↓

Prompt Builder

Result:

✔ Pipeline Test Passed

The generated prompt correctly included:

- Database schema
- Tables
- Relationships
- Natural language question
- Standardized instructions

Dataset verification:

Questions : 1034

Databases : 166

This confirms that the baseline data processing pipeline is functioning correctly.

---

# Repository Improvements

Additional improvements completed today:

- Added src/__init__.py
- Added tests/__init__.py
- Added experiments/__init__.py
- Added .gitignore
- Added requirements.txt
- Added README.md
- Added config.py
- Created tests directory
- Created documentation directory

These changes make the repository cleaner and closer to production-quality research software.

---

# Current Research Status

Completed

✔ Dataset Download

✔ Dataset Verification

✔ Dataset Optimization

✔ Repository Architecture

✔ Dataset Loader

✔ Schema Extractor

✔ Schema Formatter

✔ Prompt Builder

✔ Prompt Templates

✔ Data Models

✔ Integration Testing

Pending

⬜ Model Runner

⬜ Ollama Integration

⬜ SQL Executor

⬜ Evaluator

⬜ Baseline Experiments

⬜ Few-Shot Prompting

⬜ Chain-of-Thought Prompting

⬜ Schema Pruning

⬜ Execution Feedback

⬜ Final Evaluation

---

# Important Methodological Decisions

After evaluating multiple deployment options, the following strategy was finalized.

Inference Backend

- Ollama

Development Environment

- Local VS Code

Experiment Environment

- Google Colab GPU

Reasoning

Using fixed local open-weight checkpoints through Ollama provides better reproducibility than relying on changing third-party APIs.

The Colab runtime will be used only for inference acceleration while preserving identical model checkpoints throughout the experiments.

---

# Next Phase (Sprint 2)

The next stage of the project begins with LLM integration.

Planned workflow:

Question

↓

Prompt Builder

↓

Ollama

↓

Generated SQL

↓

SQLite Execution

↓

Execution Accuracy

↓

Results Logging

Once this pipeline is functional, the project transitions from framework development to experimental evaluation.

---

# Plan for Day 3

Objectives:

1. Prepare the Google Colab execution environment.
2. Create a reproducible setup notebook.
3. Install Ollama inside Colab.
4. Download the first target model (Qwen2.5-Coder-7B).
5. Build the initial ModelRunner.
6. Generate the first SQL query using the Spider benchmark.
7. Verify end-to-end execution from prompt generation to SQL output.

Expected milestone:

Question

↓

Prompt

↓

LLM

↓

Generated SQL

This marks the beginning of the experimental phase of the research.

---

# Summary

Day 2 focused on establishing a robust and reproducible research framework rather than rushing into model inference.

The project now has:

- A stable repository structure
- Modular architecture
- Standardized prompt system
- Structured data models
- Verified data processing pipeline
- Reproducible prompt generation

With the foundational infrastructure complete and tested, the project is now ready to enter the LLM experimentation phase.