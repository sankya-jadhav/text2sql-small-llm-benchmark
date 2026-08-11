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

    questions = [
        "How many singers do we have?",
        "What are the different countries with singers above age 20?",
        "Show all countries and the number of singers in each country.",
        "How many concerts occurred in 2014 or 2015?",
        "What are all the song names by singers who are older than average?"
    ]

    for question in questions:

        print("\n" + "=" * 60)
        print("Question:", question)

        pruned_schema = pruner.prune(
            schema,
            question
        )

        print("Original tables:")
        print(list(schema["tables"].keys()))

        print("Pruned tables:")
        print(list(pruned_schema["tables"].keys()))

        print(
            "Original columns:",
            schema["metadata"]["column_count"]
        )

        print(
            "Pruned columns:",
            pruned_schema["metadata"]["column_count"]
        )

        assert pruned_schema is not None
        assert len(pruned_schema["tables"]) > 0

if __name__ == "__main__":
    test_schema_pruner()