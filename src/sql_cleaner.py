import re


class SQLCleaner:

    @staticmethod
    def _normalize(sql: str) -> str:
        """
        Normalize SQL before execution.
        """

        sql = sql.strip()

        # Remove all trailing semicolons
        sql = re.sub(r";+\s*$", "", sql)

        return sql.strip()


    @staticmethod
    def clean(text: str) -> str:

        if not text:
            return ""

        text = text.strip()

        # ---------------------------------------
        # Case 1: ```sql ... ```
        # ---------------------------------------

        match = re.search(
            r"```sql\s*(.*?)```",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        if match:
            return SQLCleaner._normalize(
                match.group(1)
            )

        # ---------------------------------------
        # Case 2: ``` ... ```
        # ---------------------------------------

        match = re.search(
            r"```\s*(.*?)```",
            text,
            flags=re.DOTALL
        )

        if match:
            return SQLCleaner._normalize(
                match.group(1)
            )

        # ---------------------------------------
        # Case 3: Extract SQL starting with SELECT
        # ---------------------------------------

        match = re.search(
            r"\b(SELECT\b[\s\S]*)",
            text,
            flags=re.IGNORECASE
        )

        if match:
            text = match.group(1)

        # ---------------------------------------
        # Keep only first statement
        # ---------------------------------------

        text = text.strip()

        if ";" in text:
            text = text.split(";")[0]

        return SQLCleaner._normalize(text)