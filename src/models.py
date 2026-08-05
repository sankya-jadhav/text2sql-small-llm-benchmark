from dataclasses import dataclass


# ==========================================================
# LLM Generation Result
# ==========================================================

@dataclass
class GenerationResult:
    model_name: str
    prompt_type: str
    prompt: str
    generated_sql: str
    latency: float
    success: bool
    error: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


# ==========================================================
# SQL Execution Result
# ==========================================================

@dataclass
class ExecutionResult:
    success: bool
    rows: list
    execution_time: float
    error: str | None = None


# ==========================================================
# Evaluation Result (One Experiment Record)
# ==========================================================

@dataclass
class EvaluationResult:

    # Question Information
    question_id: int
    db_id: str
    question: str

    # Experiment Information
    model_name: str
    prompt_type: str
    prompt_version: str

    # Generated Output
    generated_sql: str
    gold_sql: str

    # Evaluation Metrics
    execution_accuracy: bool
    exact_match: bool
    valid_sql: bool

    # Execution Results
    gold_result: list
    generated_result: list

    # Performance Metrics
    latency: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None

    # Error Information
    error: str | None = None


# ==========================================================
# Complete Experiment Record
# ==========================================================

@dataclass
class ExperimentResult:
    question_id: int
    db_id: str
    question: str
    gold_sql: str
    generation: GenerationResult
    execution_success: bool
    execution_accuracy: bool
    execution_error: str | None = None