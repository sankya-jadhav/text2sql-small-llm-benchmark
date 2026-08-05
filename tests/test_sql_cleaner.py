from src.sql_cleaner import SQLCleaner


test_cases = [

    # Case 1 - Markdown SQL block
    """```sql
SELECT COUNT(*) FROM singer;
```""",

    # Case 2 - Plain SQL
    """SELECT COUNT(*) FROM singer;""",

    # Case 3 - Explanation + SQL
    """
Here is the SQL query:

SELECT COUNT(*) FROM singer;

This query counts all singers.
""",

    # Case 4 - Generic code block
    """```
SELECT COUNT(*) FROM singer;
```"""

]


for i, text in enumerate(test_cases, start=1):

    print("=" * 60)
    print(f"Case {i}")

    cleaned = SQLCleaner.clean(text)

    print(cleaned)