from src.schema_extractor import SchemaExtractor
from src.schema_pruner import SchemaPruner
from config import TABLES_JSON
from src.dataset_loader import DatasetLoader


def test_schema_pruner():

    loader = DatasetLoader(
        "data/dev.json",
        TABLES_JSON
    )

    extractor = SchemaExtractor(
        loader.tables_data
    )

    pruner = SchemaPruner()

    schema = extractor.get_schema(
        "concert_singer"
    )

    question = "How many singers do we have?"

    pruned_schema = pruner.prune(
        schema,
        question
    )

    print("\nOriginal tables:")
    print(
        list(schema["tables"].keys())
    )

    print("\nPruned tables:")
    print(
        list(pruned_schema["tables"].keys())
    )

    assert pruned_schema is not None
    assert len(pruned_schema["tables"]) > 0