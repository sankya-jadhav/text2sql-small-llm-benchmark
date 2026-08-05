class Evaluator:

    def execution_accuracy(
        self,
        gold_result,
        generated_result
    ) -> bool:

        if not generated_result.success:
            return False

        return gold_result.rows == generated_result.rows


    def exact_match(
        self,
        gold_sql: str,
        generated_sql: str
    ) -> bool:

        gold = " ".join(
            gold_sql.lower().split()
        )

        pred = " ".join(
            generated_sql.lower().split()
        )

        return gold == pred


    def valid_sql(
        self,
        execution_result
    ) -> bool:

        return execution_result.success