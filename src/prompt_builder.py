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

    def build_zero_shot(
        self,
        schema: str,
        question: str,
        version: str = "v1"
    ) -> str:
        """
        Build a Zero-Shot prompt.

        Parameters
        ----------
        schema : str
            Formatted database schema.

        question : str
            Natural language question.

        version : str
            Prompt version (v1, v2, ...).
        """

        template = self._load_template(
            f"zero_shot_{version}.txt"
        )

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
    
    def build(
        self,
        strategy: str,
        schema: str,
        question: str,
        version: str = "v2"
    ):

        builders = {
            "zero_shot": lambda: self.build_zero_shot(
                schema,
                question,
                version
            ),
            "few_shot": lambda: self.build_few_shot(
                schema,
                question
            ),
            "cot": lambda: self.build_cot(
                schema,
                question
            ),
            "schema_pruning": lambda: self.build_schema_pruning(
                schema,
                question
            ),
            "hybrid": lambda: self.build_hybrid(
                schema,
                question
            )
        }

        if strategy not in builders:
            raise ValueError(
                f"Unknown strategy: {strategy}"
            )

        return builders[strategy]() 