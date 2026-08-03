import json

# -------------------------
# Load Spider files
# -------------------------
with open("data/dev.json", "r", encoding="utf-8") as f:
    dev = json.load(f)

with open("data/tables.json", "r", encoding="utf-8") as f:
    tables = json.load(f)

# -------------------------
# Take first question
# -------------------------
sample = dev[0]

db_id = sample["db_id"]

print("=" * 60)
print("Question:")
print(sample["question"])

print("\nDatabase:")
print(db_id)

print("=" * 60)

# -------------------------
# Find matching schema
# -------------------------
for db in tables:

    if db["db_id"] == db_id:

        print("\nTables\n")

        table_names = db["table_names_original"]

        column_names = db["column_names_original"]

        for table_index, table_name in enumerate(table_names):

            print(f"Table: {table_name}")

            for col_table_id, col_name in column_names:

                if col_table_id == table_index:

                    print(f"   - {col_name}")

            print()

        break