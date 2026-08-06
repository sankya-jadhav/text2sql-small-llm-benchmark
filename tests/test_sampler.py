from config import DEV_JSON, TABLES_JSON

from src.dataset_loader import DatasetLoader
from src.sampler import StratifiedSampler
from config import DATABASE_ROOT
from src.database_manager import DatabaseManager

loader = DatasetLoader(
    DEV_JSON,
    TABLES_JSON
)

loader.load()

manager = DatabaseManager(DATABASE_ROOT)

available = manager.get_available_databases()

questions = loader.get_available_questions(
    available
)

sampler = StratifiedSampler(
    questions=questions,
    sample_size=180,
    random_seed=42
)

sampled = sampler.sample()

print("=" * 60)
print("STRATIFIED SAMPLER TEST")
print("=" * 60)

print(f"Total Questions Sampled : {len(sampled)}")

print(f"Unique Questions        : {len(set(sampled))}")

print(f"Duplicates              : {len(sampled) != len(set(sampled))}")

print()

print("First 20 Sampled Question Indices")

print(sampled[:20])

benchmark = sampler.save(
    "data/benchmark_sample_180.json"
)

print()

print(f"Benchmark Saved : {len(benchmark)} questions")