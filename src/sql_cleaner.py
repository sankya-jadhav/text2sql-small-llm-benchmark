import re


class SQLCleaner:

    @staticmethod
    def clean(text: str) -> str:

        if not text:
            return ""

        text = text.strip()

        # ---------------------------------------
        # Case 1 : ```sql ... ```
        # ---------------------------------------

        match = re.search(
            r"```sql\s*(.*?)```",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        # ---------------------------------------
        # Case 2 : ``` ... ```
        # ---------------------------------------

        match = re.search(
            r"```\s*(.*?)```",
            text,
            flags=re.DOTALL
        )

        if match:
            return match.group(1).strip()

        # ---------------------------------------
        # Case 3 : First SQL statement
        # ---------------------------------------

        match = re.search(
            r"(SELECT[\s\S]*?;)",
            text,
            flags=re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        return text