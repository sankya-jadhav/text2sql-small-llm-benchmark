import json

with open("data/dev.json", "r", encoding="utf-8") as f:
    dev = json.load(f)

sample = dev[0]

print("Question:")
print(sample["question"])

print("\nDatabase:")
print(sample["db_id"])

print("\nGold SQL:")
print(sample["query"])