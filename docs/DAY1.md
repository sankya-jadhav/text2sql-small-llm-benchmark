# Day 1 Progress Report
## IEEE Research Project

**Student:** Sanket Sanjay Jadhav  
**Program:** Master of Computer Applications (MCA)  
**Research Area:** Text-to-SQL using Small Open-Weight Large Language Models

---

# Proposed Research Title

**Empirical Benchmarking of Small Open-Weights LLMs in Text-to-SQL: A Lightweight Schema Pruning and Execution-Feedback Approach**

---

# Research Objective

The objective of this research is to evaluate the performance of modern small open-weight Large Language Models (LLMs) for Text-to-SQL generation while proposing a lightweight hybrid approach that improves execution accuracy with minimal computational overhead.

Unlike heavy multi-agent frameworks, this research aims to build a lightweight and reproducible pipeline suitable for local deployment and academic benchmarking.

---

# Research Methodology

The project is divided into five phases.

## Phase 1
Dataset Understanding & Framework Development

- Download Spider Dataset
- Study dataset structure
- Build reusable framework
- Understand database schemas

## Phase 2
Baseline System

- Prompt Builder
- LLM Integration
- SQL Execution
- Evaluation Pipeline

## Phase 3
Proposed Method

- Lightweight Schema Pruning
- Relevant Table Selection
- Prompt Optimization

## Phase 4
Execution Feedback

- SQL Execution
- Error Detection
- One-step Self Correction

## Phase 5
Evaluation

- Benchmark all models
- Compare prompting techniques
- Generate plots
- Write IEEE paper

---

# Overall Research Architecture

```

Spider Dataset

│

▼

Dataset Loader

│

▼

Schema Extractor

│

▼

Schema Formatter

│

▼

Prompt Builder

│

▼

LLM Interface

│

▼

SQL Executor

│

▼

Evaluation Engine

│

▼

Results

```

---

# Project Directory Structure

```

Text2SQL\_Research/

│

├── data/
│   ├── dev.json
│   ├── tables.json
│   └── database/

│

├── src/
│   ├── dataset_loader.py
│   ├── schema_extractor.py
│   ├── schema_formatter.py
│   ├── prompt_builder.py
│   ├── llm/
│   │     ├── base_llm.py
│   │     ├── ollama_llm.py
│   │     └── groq_llm.py
│   ├── sql_executor.py
│   ├── evaluator.py
│   └── utils.py

│

├── prompts/

├── experiments/

├── results/

├── notebooks/

└── main.py

```

---

# Dataset Selection

Dataset Selected

**Spider 1.0 Benchmark Dataset**

Reason

- Standard benchmark for Text-to-SQL
- SQLite databases included
- Used by most published research
- Suitable for benchmarking small LLMs

Dataset Statistics

- Development Questions: 1034
- Databases: 166
- Multiple domains
- SQLite databases

---

# Modules Completed (Day 1)

## 1. Dataset Loader ✅

Implemented a reusable DatasetLoader class.

Responsibilities

- Load dev.json
- Load tables.json
- Return individual questions
- Return dataset statistics

Verified Output

- Questions: 1034
- Databases: 166

---

## 2. Schema Extractor ✅

Implemented SchemaExtractor.

Extracts

- Database Name
- Table Names
- Column Names
- Primary Keys
- Foreign Keys
- Metadata

Example

```

Database: concert\_singer

Tables

singer
Name
Country
Age

concert
...

Relationships

concert.Stadium\_ID -> stadium.Stadium\_ID

```

---

## 3. Schema Formatter ✅

Implemented SchemaFormatter.

Converts structured schema into LLM-readable text.

Output

```

Database: concert\_singer

Tables

Table: singer

- Singer\_ID
- Name
- Country

Relationships

concert.Stadium\_ID -> stadium.Stadium\_ID

```

This formatted schema will be used by all prompting strategies.

---

# Current Status

Completed

- Dataset Download
- Dataset Verification
- SQLite Verification
- Dataset Loader
- Schema Extractor
- Schema Formatter

Pending

- Prompt Builder
- LLM Interface
- SQL Executor
- Evaluator
- Schema Pruner
- Execution Feedback
- Experiments

---

# Planned Experimental Pipeline

Question

↓

Schema Extractor

↓

Schema Formatter

↓

Prompt Builder

↓

LLM

↓

Generated SQL

↓

SQLite Execution

↓

Evaluation

---

# Models Planned

- Qwen2.5-Coder-7B-Instruct
- DeepSeek-Coder-6.7B-Instruct
- Llama-3.1-8B-Instruct

Inference Backend

- Ollama (Development)
- Groq API (Large-scale Experiments)

---

# Planned Prompting Strategies

1. Zero-Shot Prompting
2. Few-Shot Prompting
3. Chain-of-Thought Prompting
4. Schema Pruning (Proposed)
5. Hybrid Schema Pruning + Execution Feedback (Proposed)

---

# Evaluation Metrics

- Execution Accuracy
- Exact Match Accuracy
- Latency
- Token Usage
- Schema Reduction Percentage
- Correction Success Rate

---

# Novel Contribution

The proposed contribution of this research is a lightweight hybrid pipeline consisting of

1. Automatic Schema Pruning
2. One-step Execution Feedback

The objective is to improve execution accuracy while reducing prompt size and inference latency compared to heavier multi-agent approaches.

---

# Development Philosophy

The project follows a modular and reusable architecture.

Each component has a single responsibility.

Dataset Loader
↓

Schema Extractor
↓

Schema Formatter
↓

Prompt Builder
↓

LLM Interface
↓

SQL Executor
↓

Evaluator

This design allows new prompting strategies and LLMs to be added without modifying the evaluation framework.

---

# Day 1 Summary

Successfully completed the data processing layer of the research framework.

Established a reusable architecture for future experimentation.

The next milestone is implementing the Prompt Builder and integrating the first LLM to generate SQL queries on the Spider benchmark.
