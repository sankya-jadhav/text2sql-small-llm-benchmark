from src.dataset_loader import DatasetLoader
from src.schema_extractor import SchemaExtractor
from src.schema_formatter import SchemaFormatter
from src.prompt_builder import PromptBuilder

loader = DatasetLoader(
    "data/dev.json",
    "data/tables.json"
)

loader.load() 

sample = loader.get_question(0)

extractor = SchemaExtractor(loader.tables_data)
formatter = SchemaFormatter()
builder = PromptBuilder()

schema = extractor.get_schema(sample["db_id"])
schema_text = formatter.format(schema)
prompt = builder.build_zero_shot(
    schema_text,
    sample["question"]
)

print("=" * 60)
print("PIPELINE TEST PASSED")
print("=" * 60)
print(sample["question"])
print("=" * 60)
print(prompt[:500])
print(loader.get_statistics())


