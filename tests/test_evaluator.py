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