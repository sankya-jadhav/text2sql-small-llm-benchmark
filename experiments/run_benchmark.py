import json

from config import MODEL_NAME

from src.dataset_loader import DatasetLoader
from src.database_manager import DatabaseManager
from src.schema_extractor import SchemaExtractor
from src.schema_formatter import SchemaFormatter
from src.prompt_builder import PromptBuilder
from src.sql_executor import SQLExecutor
from src.execution_feedback import ExecutionFeedback
from src.sql_cleaner import SQLCleaner
from src.evaluator import Evaluator
from src.experiment_runner import ExperimentRunner
from src.hf_runner import HFRunner
from config import TEST_MODE, TEST_SIZE
from src.schema_pruner import SchemaPruner


# ==========================================================
# EXPERIMENT CONFIGURATION
# ==========================================================

STRATEGY = "zero_shot"
PROMPT_VERSION = "v3_execution_feedback"

# ==========================================================
# RESULT FILE
# ==========================================================





with open(
    "data/benchmark_sample_180.json",
    "r",
    encoding="utf-8"
) as f:

    benchmark = json.load(f)


from config import (
    MODEL_NAME,
    DEV_JSON,
    TABLES_JSON,
    DATABASE_ROOT,
    RESULTS_DIR
)

loader = DatasetLoader(
    DEV_JSON,
    TABLES_JSON
)

manager = DatabaseManager(
    DATABASE_ROOT
)



schema_extractor = SchemaExtractor(
    loader.tables_data
)



schema_pruner = SchemaPruner()

schema_formatter = SchemaFormatter()

prompt_builder = PromptBuilder()

sql_executor = SQLExecutor()

sql_cleaner = SQLCleaner()

evaluator = Evaluator()

model = HFRunner(
    MODEL_NAME
)

execution_feedback = ExecutionFeedback(
    prompt_builder=prompt_builder,
    sql_cleaner=sql_cleaner,
    sql_executor=sql_executor
)


runner = ExperimentRunner(

    loader=loader,

    database_manager=manager,

    schema_extractor=schema_extractor,

    schema_pruner=schema_pruner,

    schema_formatter=schema_formatter,

    prompt_builder=prompt_builder,

    model_runner=None,

    sql_executor=sql_executor,

    sql_cleaner=sql_cleaner,

    execution_feedback=execution_feedback,

    evaluator=evaluator

)



completed = runner.load_completed_questions(
    MODEL_NAME,
    STRATEGY,
    PROMPT_VERSION
)

print(f"Completed Questions Found : {len(completed)}")


if TEST_MODE:
    benchmark = benchmark[:TEST_SIZE]
print("=" * 60)
print("EXPERIMENT CONFIGURATION")
print("=" * 60)

print("Model          :", MODEL_NAME)
print("Strategy       :", STRATEGY)
print("Prompt Version :", PROMPT_VERSION)
print(
    "Result Directory :",
    runner.get_result_file(
        MODEL_NAME,
        STRATEGY,
        PROMPT_VERSION
    )
)

print()

print("=" * 60)
print("RUNNING BENCHMARK")
print("=" * 60)

results = []

for i, sample in enumerate(benchmark):
    print("-" * 60)
    print(f"[{i+1}/{len(benchmark)}]")
    print("Database :", sample["db_id"])
    print("Question :", sample["question"])

    question_index = loader.dev_data.index(sample)

    if question_index in completed:

        print(f"Skipping Question {question_index}")

        continue

    try:
        
        result = runner.run_question(

        question_index=question_index,

        model_runner=model,

        strategy=STRATEGY,

        prompt_version=PROMPT_VERSION,

        use_schema_pruner=True

        )

        results.append(result)

        print("Execution Accuracy :", result.execution_accuracy)
        print("Exact Match        :", result.exact_match)
        print("Valid SQL          :", result.valid_sql)
        print("Initial Execution  :", result.initial_execution_success)
        print("Was Corrected      :", result.was_corrected)
        print("Initial Error      :", result.initial_error)
        print("Latency            :", f"{result.latency:.2f}s")
        print("Feedback Latency   :", f"{result.feedback_latency:.2f}s")
        print()
    except Exception as e:

        print(f"[ERROR] Question {question_index}")

        print(e)

    print()

    if (i + 1) % 10 == 0:

        print("=" * 60)

        print(f"Completed {i + 1}/{len(benchmark)} questions")

        print("=" * 60)


correct = sum(
    r.execution_accuracy
    for r in results
)

print("=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Already Completed : {len(completed)}")
print(f"Executed This Run : {len(results)}")
print(f"Total Benchmark   : {len(benchmark)}")

correct = sum(
    r.execution_accuracy
    for r in results
)

print(f"Execution Accuracy : {correct}/{len(results)}")

import gc
import torch

del model

gc.collect()

torch.cuda.empty_cache()

print()

print("GPU Memory Released")