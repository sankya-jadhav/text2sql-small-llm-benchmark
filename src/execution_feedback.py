class ExecutionFeedback:

    def __init__(
        self,
        prompt_builder,
        sql_cleaner,
        sql_executor
    ):
        self.prompt_builder = prompt_builder
        self.sql_cleaner = sql_cleaner
        self.sql_executor = sql_executor

    def correct_sql(
        self,
        model_runner,
        database,
        schema,
        question,
        generated_sql,
        execution_error
    ):

        prompt = self.prompt_builder.build_execution_feedback(
            schema=schema,
            question=question,
            generated_sql=generated_sql,
            error=execution_error,
            version="v1"
        )

        generation = model_runner.generate(
            prompt,
            prompt_type="execution_feedback"
        )

        corrected_sql = self.sql_cleaner.clean(
            generation.generated_sql
        )

        generation.generated_sql = corrected_sql

        execution = self.sql_executor.execute(
            database,
            corrected_sql
        )

        return generation, execution