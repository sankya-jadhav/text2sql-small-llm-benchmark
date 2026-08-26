from config import TABLES_JSON
from src.dataset_loader import DatasetLoader
from src.schema_extractor import SchemaExtractor


def test_car1_schema():

    loader = DatasetLoader(
        "data/dev.json",
        TABLES_JSON
    )

    extractor = SchemaExtractor(
        loader.tables_data
    )

    schema = extractor.get_schema("car1")

    print("Schema:", schema)

    assert schema is not None, (
        "Schema for 'car1' was not found. "
        "Check DatasetLoader and SchemaExtractor."
    )

    print("\nTABLES")
    print("=" * 60)

    for table in schema["tables"]:
        print(table)

    print("\nFOREIGN KEYS")
    print("=" * 60)

    for fk in schema["foreign_keys"]:
        print(fk)


if __name__ == "__main__":
    test_car1_schema()
        