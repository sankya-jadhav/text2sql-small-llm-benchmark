from pathlib import Path


class PromptBuilder:
    """
    Builds prompts for different prompting strategies.

    Prompt templates are stored separately inside the prompts/
    directory to improve reproducibility and make prompt
    engineering easier.
    """

    def __init__(self, prompt_dir="prompts"):
        self.prompt_dir = Path(prompt_dir)

    def _load_template(self, filename: str) -> str:
        """
        Load a prompt template from the prompts directory.
        """

        template_path = self.prompt_dir / filename

        if not template_path.exists():
            raise FileNotFoundError(
                f"Prompt template not found: {template_path}"
            )

        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()

    def build_zero_shot(self, schema: str, question: str) -> str:
        """
        Build a Zero-Shot prompt.
        """

        template = self._load_template("zero_shot.txt")

        return template.format(
            schema=schema,
            question=question
        )

    # Future Prompt Types
    # ----------------------------

    def build_few_shot(self, schema: str, question: str):
        raise NotImplementedError("Few-Shot Prompt not implemented yet.")

    def build_cot(self, schema: str, question: str):
        raise NotImplementedError("Chain-of-Thought Prompt not implemented yet.")

    def build_schema_pruning(self, schema: str, question: str):
        raise NotImplementedError("Schema Pruning Prompt not implemented yet.")

    def build_hybrid(self, schema: str, question: str):
        raise NotImplementedError("Hybrid Prompt not implemented yet.")