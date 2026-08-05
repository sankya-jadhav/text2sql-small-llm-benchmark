from src.models import ExecutionResult


class Evaluator:
    """
    Evaluates generated SQL using execution accuracy.
    """

    def execution_accuracy(
        self,
        gold_result: ExecutionResult,
        predicted_result: ExecutionResult,
    ) -> bool:
        """
        Returns True if both SQL queries produce identical outputs.
        """

        # Generated SQL failed
        if not predicted_result.success:
            return False

        # Gold SQL should always succeed
        if not gold_result.success:
            raise RuntimeError(
                "Gold SQL execution failed. Dataset may be corrupted."
            )

        return gold_result.rows == predicted_result.rows