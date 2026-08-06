from src.dataset_loader import DatasetLoader
from src.database_manager import DatabaseManager
from src.schema_extractor import SchemaExtractor
from src.schema_formatter import SchemaFormatter
from src.prompt_builder import PromptBuilder
from src.hf_runner import HFRunner
from src.sql_executor import SQLExecutor
from src.evaluator import Evaluator

# --------------------------------------------------
# --------------------------------------------------
# Configuration
# --------------------------------------------------

from config import (
    DEV_JSON,
    TABLES_JSON,
    DATABASE_ROOT
)

# --------------------------------------------------
# Dataset
# --------------------------------------------------

loader = DatasetLoader(
    DEV_JSON,
    TABLES_JSON
)

loader.load()

sample = loader.get_question(0)

# --------------------------------------------------
# Database
# --------------------------------------------------

manager = DatabaseManager(
    DATABASE_ROOT
)

database = manager.get_database_path(
    sample["db_id"]
)
# --------------------------------------------------
# Prompt
# --------------------------------------------------

extractor = SchemaExtractor(loader.tables_data)

formatter = SchemaFormatter()

builder = PromptBuilder()

schema = extractor.get_schema(sample["db_id"])

schema_text = formatter.format(schema)

prompt = builder.build_zero_shot(
    schema_text,
    sample["question"]
)

# --------------------------------------------------
# Model
# --------------------------------------------------

from config import MODEL_NAME

runner = HFRunner(
    MODEL_NAME
)

generation = runner.generate(
    prompt,
    "zero-shot"
)

# --------------------------------------------------
# Execute SQL
# --------------------------------------------------

executor = SQLExecutor()

generated_result = executor.execute(
    database,
    generation.generated_sql
)

gold_result = executor.execute(
    database,
    sample["query"]
)

# --------------------------------------------------
# Evaluate
# --------------------------------------------------

evaluator = Evaluator()

accuracy = evaluator.execution_accuracy(
    gold_result,
    generated_result
)

# --------------------------------------------------
# Print
# --------------------------------------------------

print("=" * 70)

print("Question")
print(sample["question"])

print("\nGold SQL")
print(sample["query"])

print("\nGenerated SQL")
print(generation.generated_sql)

print("\nGold Result")
print(gold_result.rows)

print("\nGenerated Result")
print(generated_result.rows)

print("\nExecution Accuracy")
print(accuracy)