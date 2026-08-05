from src.models import ExecutionResult
from src.evaluator import Evaluator

gold = ExecutionResult(
    success=True,
    rows=[(6,)],
    execution_time=0.01
)

prediction = ExecutionResult(
    success=True,
    rows=[(6,)],
    execution_time=0.03
)

evaluator = Evaluator()

print("Case 1:", evaluator.execution_accuracy(
    gold,
    prediction
))

prediction = ExecutionResult(
    success=True,
    rows=[(5,)],
    execution_time=0.03
)

print("Case 2:", evaluator.execution_accuracy(
    gold,
    prediction
))

prediction = ExecutionResult(
    success=False,
    rows=[],
    execution_time=0.02,
    error="no such table"
)

print("Case 3:", evaluator.execution_accuracy(
    gold,
    prediction
))

print("\nExact Match Tests")
print("-" * 30)

gold_sql = "SELECT COUNT(*) FROM singer;"

generated_sql = "SELECT COUNT(*) FROM singer;"

print(
    evaluator.exact_match(
        gold_sql,
        generated_sql
    )
)

generated_sql = "SELECT COUNT(Singer_ID) FROM singer;"

print(
    evaluator.exact_match(
        gold_sql,
        generated_sql
    )
)

print("\nValid SQL Tests")
print("-" * 30)

from src.models import ExecutionResult

success_result = ExecutionResult(
    success=True,
    rows=[],
    execution_time=0.01
)

failed_result = ExecutionResult(
    success=False,
    rows=[],
    execution_time=0.01,
    error="syntax error"
)

print(
    evaluator.valid_sql(
        success_result
    )
)

print(
    evaluator.valid_sql(
        failed_result
    )
)