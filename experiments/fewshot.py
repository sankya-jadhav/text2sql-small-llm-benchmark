import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dataset_loader import DatasetLoader
from src.schema_extractor import SchemaExtractor
from src.schema_formatter import SchemaFormatter
from src.prompt_builder import PromptBuilder
from src.model_runner import ModelRunner

def run_fewshot_experiment():
    print("Initializing Few-Shot Experiment...")
    # Load dataset
    loader = DatasetLoader("data/dev.json", "data/tables.json")
    loader.load()
    print(f"Loaded {loader.total_questions()} questions and {loader.total_databases()} databases.")

    # Initialize components
    extractor = SchemaExtractor(loader.tables_data)
    formatter = SchemaFormatter()
    builder = PromptBuilder()

    # TODO: Implement few-shot prompt construction and evaluation loop
    print("Few-shot experiment setup ready.")

if __name__ == "__main__":
    run_fewshot_experiment()
