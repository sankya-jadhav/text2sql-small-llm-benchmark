from src.dataset_loader import DatasetLoader
from src.database_manager import DatabaseManager
from src.schema_extractor import SchemaExtractor
from src.schema_formatter import SchemaFormatter
from src.prompt_builder import PromptBuilder
from src.hf_runner import HFRunner
from src.sql_executor import SQLExecutor
from src.evaluator import Evaluator
from src.experiment_runner import ExperimentRunner


loader = DatasetLoader(
    "data/dev.json",
    "data/tables.json"
)
loader.load()

manager = DatabaseManager("data/database")

runner = ExperimentRunner(

    loader=loader,

    database_manager=manager,

    schema_extractor=SchemaExtractor(loader.tables_data),

    schema_formatter=SchemaFormatter(),

    prompt_builder=PromptBuilder(),

    model_runner=HFRunner(
        "Qwen/Qwen2.5-0.5B-Instruct"
    ),

    sql_executor=SQLExecutor(),

    evaluator=Evaluator(),

    result_dir="results/test"
)

sample = loader.get_question(0)

print(sample["db_id"])

print(
    manager.get_database_path(
        sample["db_id"]
    )
)

result = runner.run_question(
    question_index=0,
    strategy="zero_shot",
    prompt_version="v2"
)

print(result)