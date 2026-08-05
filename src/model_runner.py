from abc import ABC, abstractmethod

from src.models import GenerationResult


class ModelRunner(ABC):
    """
    Abstract interface for all LLM backends.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate(
        self,
        prompt: str,
        prompt_type: str
    ) -> GenerationResult:
        """
        Generate SQL from a prompt.
        """
        pass