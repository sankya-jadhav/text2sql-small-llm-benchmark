from src.dataset_loader import DatasetLoader

loader = DatasetLoader(
    "data/dev.json",
    "data/tables.json"
)

loader.load()

print(loader.total_questions())
print(loader.total_databases())

sample = loader.get_question(0)

print(sample["question"])