
import json
from pathlib import Path
from config import RESULTS_DIR
from src.models import EvaluationResult

class ExperimentRunner:

    def __init__(

        self,
        loader,
        database_manager,
        schema_extractor,
        schema_pruner,
        schema_formatter,
        prompt_builder,
        model_runner,
        sql_executor,
        sql_cleaner,
        execution_feedback,
        evaluator,
        result_dir=RESULTS_DIR
    ):

        self.loader = loader

        self.database_manager = database_manager

        self.schema_extractor = schema_extractor

        self.schema_pruner = schema_pruner

        self.schema_formatter = schema_formatter

        self.prompt_builder = prompt_builder

        self.model_runner = model_runner

        self.sql_executor = sql_executor

        self.sql_cleaner = sql_cleaner
        self.execution_feedback = execution_feedback

        self.evaluator = evaluator

        self.result_dir = Path(result_dir)


    def save_result(
        self,
        result: EvaluationResult,
        result_name: str | None = None
    ):

        output_file = self.get_result_file(
            result.model_name,
            result_name or result.prompt_type
        )

        with open(
            output_file,
            "a",
            encoding="utf-8"
        ) as f:

            json.dump(
                result.__dict__,
                f
            )

            f.write("\n")

    def run_question(
        self,
        question_index: int,
        model_runner,
        strategy: str = "zero_shot",
        prompt_version: str = "v2",
        use_schema_pruner: bool = False,
        result_name: str | None = None
    ):

        sample = self.loader.get_question(
            question_index
        )

        database = self.database_manager.get_database_path(
            sample["db_id"]
        )

        # Get full schema
        schema = self.schema_extractor.get_schema(
            sample["db_id"]
        )

        # Prune schema based on the question
        if use_schema_pruner:
            working_schema = self.schema_pruner.prune(
                schema,
                sample["question"]
            )
        else:
            working_schema = schema
        # --------------------------------------------------
        # Schema reduction metrics
        # --------------------------------------------------

        full_schema_columns = sum(
            len(columns)
            for columns in schema["tables"].values()
        )

        pruned_schema_columns = sum(
            len(columns)
            for columns in working_schema["tables"].values()
        )

        schema_reduction_percent = (
            (
                full_schema_columns - pruned_schema_columns
            )
            / full_schema_columns
            * 100
            if full_schema_columns > 0
            else 0.0
        )

       # Format the working schema for the model
        schema_text = self.schema_formatter.format(
            working_schema
        )

        prompt = self.prompt_builder.build(
            strategy=strategy,
            schema=schema_text,
            question=sample["question"],
            version=prompt_version
        )

        # --------------------------------------------------
        # Initial SQL Generation
        # --------------------------------------------------

        generation = model_runner.generate(
            prompt,
            prompt_type=strategy
        )

        initial_sql = self.sql_cleaner.clean(
            generation.generated_sql
        )

        generation.generated_sql = initial_sql

        generated_result = self.sql_executor.execute(
            database,
            initial_sql
        )

        # --------------------------------------------------
        # Execution Feedback
        # --------------------------------------------------

        initial_execution_success = generated_result.success
        initial_error = generated_result.error

        corrected_sql = None
        was_corrected = False

        feedback_latency = 0.0
        feedback_prompt_tokens = None
        feedback_completion_tokens = None
        feedback_total_tokens = None

        if not generated_result.success:

            feedback_generation, feedback_result = (
                self.execution_feedback.correct_sql(
                    model_runner=model_runner,
                    database=database,
                    schema=schema_text,
                    question=sample["question"],
                    generated_sql=initial_sql,
                    execution_error=generated_result.error
                )
            )

            corrected_sql = feedback_generation.generated_sql

            generated_result = feedback_result

            was_corrected = True

            feedback_latency = feedback_generation.latency
            feedback_prompt_tokens = feedback_generation.prompt_tokens
            feedback_completion_tokens = feedback_generation.completion_tokens
            feedback_total_tokens = feedback_generation.total_tokens

            generation.generated_sql = corrected_sql



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

            # Execution Feedback
            initial_sql=initial_sql,
            corrected_sql=corrected_sql,
            initial_error=initial_error,
            initial_execution_success=initial_execution_success,
            was_corrected=was_corrected,

            feedback_latency=feedback_latency,
            feedback_prompt_tokens=feedback_prompt_tokens,
            feedback_completion_tokens=feedback_completion_tokens,
            feedback_total_tokens=feedback_total_tokens,

            
            # Schema pruning metrics
            full_schema_columns=full_schema_columns,
            pruned_schema_columns=pruned_schema_columns,
            schema_reduction_percent=schema_reduction_percent,

            # Errors
            error=generated_result.error
        )


        self.save_result(result,result_name=result_name)

        return result


    def get_result_file(
        self,
        model_name,
        result_name
    ):
        """
        Returns the JSONL file for one experiment.
        """

        safe_model = model_name.split("/")[-1]

        model_dir = self.result_dir / safe_model

        model_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        return model_dir / f"{result_name}.jsonl"


    def load_completed_questions(
        self,
        model_name,
        result_name
    ):
        """
        Returns all completed question ids.
        """

        completed = set()

        result_file = self.get_result_file(
            model_name,
            result_name
        )

        if not result_file.exists():
            return completed

        with open(
            result_file,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                data = json.loads(line)

                completed.add(
                    data["question_id"]
                )

        return completed
