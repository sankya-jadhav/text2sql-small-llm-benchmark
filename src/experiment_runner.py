from huggingface_hub.inference._generated.types import zero_shot_image_classification
from main import schema_text
from huggingface_hub.inference._generated.types import zero_shot_image_classification
import json
from pathlib import Path
from dataclasses import asdict
from config import RESULTS_DIR
from src.models import EvaluationResult


class ExperimentRunner:

    def __init__(
        self,
        loader,
        database_manager,
        schema_extractor,
        schema_formatter,
        prompt_builder,
        model_runner,
        sql_executor,
        evaluator,
        result_dir=RESULTS_DIR
    ):

        self.loader = loader

        self.database_manager = database_manager

        self.schema_extractor = schema_extractor

        self.schema_formatter = schema_formatter

        self.prompt_builder = prompt_builder

        self.model_runner = model_runner

        self.sql_executor = sql_executor

        self.evaluator = evaluator

        self.result_dir = Path(result_dir)


    def save_result(
        self,
        result: EvaluationResult
    ):

        self.result_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = self.result_dir / f"{result.question_id:04d}.json"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                asdict(result),
                f,
                indent=4
            )

    def run_question(
        self,
        question_index: int,
        model_runner,
        strategy: str = "zero_shot",
        prompt_version: str = "v2"
    ):

        sample = self.loader.get_question(
            question_index
        )

        database = self.database_manager.get_database_path(
            sample["db_id"]
        )

        schema = self.schema_extractor.get_schema(
            sample["db_id"]
        )

        schema_text = self.schema_formatter.format(
            schema
        )

        prompt = self.prompt_builder.build(
            strategy=strategy,
            schema=schema_text,
            question=sample["question"],
            version=prompt_version
        )

        generation = model_runner.generate(
            prompt,
            prompt_type=strategy
        )

        generated_result = self.sql_executor.execute(
            database,
            generation.generated_sql
        )

        gold_result = self.sql_executor.execute(
            database,
            sample["query"]
        )

        execution_accuracy = self.evaluator.execution_accuracy(
            gold_result,
            generated_result
        )

        exact_match = self.evaluator.exact_match(
            sample["query"],
            generation.generated_sql
        )

        valid_sql = self.evaluator.valid_sql(
            generated_result
        )

        result = EvaluationResult(

            # Question
            question_id=question_index,
            db_id=sample["db_id"],
            question=sample["question"],

            # Experiment
            model_name=generation.model_name,
            prompt_type=strategy,
            prompt_version=prompt_version,

            # SQL
            generated_sql=generation.generated_sql,
            gold_sql=sample["query"],

            # Metrics
            execution_accuracy=execution_accuracy,
            exact_match=exact_match,
            valid_sql=valid_sql,

            # Execution Results
            gold_result=gold_result.rows,
            generated_result=generated_result.rows,

            # Performance
            latency=generation.latency,
            prompt_tokens=generation.prompt_tokens,
            completion_tokens=generation.completion_tokens,
            total_tokens=generation.total_tokens,

            # Errors
            error=generated_result.error
        )


        self.save_result(result)

        return result
