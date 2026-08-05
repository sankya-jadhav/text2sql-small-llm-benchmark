from src.dataset_loader import DatasetLoader
from src.database_manager import DatabaseManager
from src.schema_extractor import SchemaExtractor
from src.schema_formatter import SchemaFormatter
from src.prompt_builder import PromptBuilder
from src.sql_executor import SQLExecutor

print("=" * 70)
print("TEXT-TO-SQL PIPELINE TEST")
print("=" * 70)

# -------------------------
# Dataset
# -------------------------

loader = DatasetLoader(
    "data/dev.json",
    "data/tables.json"
)

manager = DatabaseManager("data/database")

available = manager.get_available_databases()

questions = loader.get_available_questions(available)

print(f"Available databases : {len(available)}")
print(f"Runnable questions  : {len(questions)}")

# -------------------------
# First sample
# -------------------------

sample = questions[0]

print("\nQuestion:")
print(sample["question"])

print("\nDatabase:")
print(sample["db_id"])

# -------------------------
# Schema
# -------------------------

extractor = SchemaExtractor(loader.tables_data)

schema = extractor.get_schema(sample["db_id"])

formatter = SchemaFormatter()

schema_text = formatter.format(schema)

# -------------------------
# Prompt
# -------------------------

builder = PromptBuilder()

prompt = builder.build_zero_shot(
    schema_text,
    sample["question"]
)

print("\nPrompt Preview")
print("-" * 70)

print(prompt[:400])

# -------------------------
# SQL Execution
# -------------------------

executor = SQLExecutor()

database = manager.get_database_path(
    sample["db_id"]
)

result = executor.execute(
    database,
    sample["query"]
)

print("\nGold SQL")
print("-" * 70)

print(sample["query"])

print("\nExecution Result")
print("-" * 70)

print(result)

print("\n")

print("=" * 70)
print("PIPELINE TEST PASSED")
print("=" * 70)

from src.evaluator import Evaluator

# Simulate a perfect model by using the gold SQL
generated_result = executor.execute(
    database,
    sample["query"]
)

evaluator = Evaluator()

accuracy = evaluator.execution_accuracy(
    result,
    generated_result
)

print("\nExecution Accuracy")
print("-" * 50)
print(accuracy)