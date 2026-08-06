from src.hf_runner import HFRunner

from config import MODEL_NAME

runner = HFRunner(
    MODEL_NAME
)

result = runner.generate(
    prompt="Write SQL to count all singers from table singer.",
    prompt_type="test"
)

print(result)