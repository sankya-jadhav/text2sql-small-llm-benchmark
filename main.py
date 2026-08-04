from src.dataset_loader import DatasetLoader
from src.schema_extractor import SchemaExtractor

loader = DatasetLoader(
    "data/dev.json",
    "data/tables.json"
)

loader.load()

sample = loader.get_question(0)

extractor = SchemaExtractor(loader.tables_data)

schema = extractor.get_schema(sample["db_id"])

print("\nTables\n")

for table, cols in schema["tables"].items():

    print(table)

    for c in cols:

        print("   ", c)

print("\nPrimary Keys\n")

for pk in schema["primary_keys"]:

    print(pk)

print("\nForeign Keys\n")

for fk in schema["foreign_keys"]:

    print(fk)

from src.schema_formatter import SchemaFormatter

formatter = SchemaFormatter()

schema_text = formatter.format(schema)

print(schema_text)

from src.prompt_builder import PromptBuilder

builder = PromptBuilder()

prompt = builder.build_zero_shot(
    schema_text,
    sample["question"]
)

with open("prompts/zero_shot_example.txt", "w", encoding="utf-8") as f:
    f.write(prompt)