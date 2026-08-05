from dataclasses import dataclass


@dataclass
class GenerationResult:
    model_name: str
    prompt_type: str
    prompt: str
    generated_sql: str
    latency: float
    success: bool
    error: str | None = None


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

@dataclass
class ExecutionResult:

    success: bool

    rows: list

    execution_time: float

    error: str | None = None