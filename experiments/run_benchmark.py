import json

from config import MODEL_NAME

from src.dataset_loader import DatasetLoader
from src.database_manager import DatabaseManager
from src.schema_extractor import SchemaExtractor
from src.schema_formatter import SchemaFormatter
from src.prompt_builder import PromptBuilder
from src.sql_executor import SQLExecutor
from src.evaluator import Evaluator
from src.experiment_runner import ExperimentRunner
from src.hf_runner import HFRunner


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
    DATABASE_ROOT
)

loader = DatasetLoader(
    DEV_JSON,
    TABLES_JSON
)

manager = DatabaseManager(
    DATABASE_ROOT
)

runner = ExperimentRunner(

    loader=loader,

    database_manager=manager,

    schema_extractor=SchemaExtractor(
        loader.tables_data
    ),

    schema_formatter=SchemaFormatter(),

    prompt_builder=PromptBuilder(),

    model_runner=None,

    sql_executor=SQLExecutor(),

    evaluator=Evaluator()

)

model = HFRunner(
    MODEL_NAME
)

completed = runner.load_completed_questions(
    MODEL_NAME,
    "zero_shot",
    "v2"
)

print(f"Completed Questions Found : {len(completed)}")

TEST_MODE = True
TEST_SIZE = 5
if TEST_MODE:
    benchmark = benchmark[:TEST_SIZE]

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


    result = runner.run_question(

        question_index=question_index,

        model_runner=model,

        strategy="zero_shot",

        prompt_version="v2"

    )

    results.append(result)

    print("Execution Accuracy :", result.execution_accuracy)
    print("Exact Match        :", result.exact_match)
    print("Latency            :", f"{result.latency:.2f}s")
    print()


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