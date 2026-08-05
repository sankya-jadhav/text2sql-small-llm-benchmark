from src.model_runner import ModelRunner
from src.models import GenerationResult


class OllamaRunner(ModelRunner):
    """
    Ollama implementation of ModelRunner.
    """

    def generate(
        self,
        prompt: str,
        prompt_type: str
    ) -> GenerationResult:

        raise NotImplementedError(
            "Ollama inference will be implemented after Colab setup."
        )