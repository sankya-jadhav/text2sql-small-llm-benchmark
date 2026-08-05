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
    question_id: int
    db_id: str 
    model_name: str
    prompt_type: str
    execution_accuracy: bool
    latency: float
    generated_sql: str
    gold_sql: str
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