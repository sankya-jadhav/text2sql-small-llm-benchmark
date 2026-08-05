from src.hf_runner import HFRunner

runner = HFRunner(
    model_name="Qwen/Qwen2.5-0.5B-Instruct"
)

result = runner.generate(
    prompt="Write SQL to count all singers from table singer.",
    prompt_type="test"
)

print(result)