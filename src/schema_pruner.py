import re

from src.logger import get_logger


logger = get_logger(__name__)


class SchemaPruner:

    def __init__(self):
        pass

    def prune(self, schema, question):
        """
        Prune irrelevant tables and columns from a database schema
        based on keywords present in the natural-language question.

        The pruner is intentionally conservative:
        if no relevant table can be identified, the full schema is returned.
        """

        question_lower = question.lower()

        relevant_tables = set()

        # --------------------------------------------------
        # 1. Identify tables mentioned in the question
        # --------------------------------------------------

        for table_name in schema["tables"]:

            table_lower = table_name.lower()

            if self._matches_keyword(
                table_lower,
                question_lower
            ):
                relevant_tables.add(table_name)

        # --------------------------------------------------
        # 2. Identify columns mentioned in the question
        # --------------------------------------------------

        for table_name, columns in schema["tables"].items():

            for column in columns:

                column_lower = column.lower()

                if self._matches_keyword(
                    column_lower,
                    question_lower
                ):
                    relevant_tables.add(table_name)

        # --------------------------------------------------
        # 3. If nothing was identified, keep full schema
        # --------------------------------------------------

        if not relevant_tables:

            logger.debug(
                "No relevant tables found. "
                "Returning full schema."
            )

            return schema

        # --------------------------------------------------
        # 4. Preserve tables required for foreign-key joins
        # --------------------------------------------------

        # Do not automatically expand through every FK relationship.
        # Join-table preservation will be handled separately.

        # --------------------------------------------------
        # 5. Build pruned schema
        # --------------------------------------------------

        pruned_schema = {
            "database": schema["database"],
            "tables": {},
            "primary_keys": [],
            "foreign_keys": [],
            "metadata": dict(schema.get("metadata", {}))
        }

        for table_name in relevant_tables:

            if table_name in schema["tables"]:

                pruned_schema["tables"][table_name] = (
                    schema["tables"][table_name]
                )

        # --------------------------------------------------
        # 6. Keep relevant primary keys
        # --------------------------------------------------

        for pk in schema["primary_keys"]:

            if pk["table"] in relevant_tables:

                pruned_schema["primary_keys"].append(pk)

        # --------------------------------------------------
        # 7. Keep relevant foreign keys
        # --------------------------------------------------

        for fk in schema["foreign_keys"]:

            if (
                fk["from_table"] in relevant_tables
                and
                fk["to_table"] in relevant_tables
            ):

                pruned_schema["foreign_keys"].append(fk)

        # --------------------------------------------------
        # 8. Update metadata
        # --------------------------------------------------

        pruned_schema["metadata"]["table_count"] = (
            len(pruned_schema["tables"])
        )

        pruned_schema["metadata"]["column_count"] = sum(
            len(columns)
            for columns in pruned_schema["tables"].values()
        )

        pruned_schema["metadata"]["primary_key_count"] = (
            len(pruned_schema["primary_keys"])
        )

        pruned_schema["metadata"]["foreign_key_count"] = (
            len(pruned_schema["foreign_keys"])
        )

        logger.debug(
            f"Original tables: "
            f"{list(schema['tables'].keys())}"
        )

        logger.debug(
            f"Pruned tables: "
            f"{list(pruned_schema['tables'].keys())}"
        )

        return pruned_schema

    # ======================================================
    # Helper Methods
    # ======================================================

    def _matches_keyword(self, schema_name, question):

        """
        Check whether a schema name appears as a meaningful
        word/phrase in the question.
        """

        # Convert underscores into spaces.
        normalized_name = schema_name.replace("_", " ")

        # Match complete words rather than arbitrary substrings.
        words = normalized_name.split()

        for word in words:

            if len(word) <= 2:
                continue

            pattern = r"\b" + re.escape(word) + r"\b"

            if re.search(pattern, question):

                return True

        return False
        if self._matches_keyword(
            column_lower,
            question_lower
        ):

            print(
                f"[PRUNER] Column match: "
                f"{table_name}.{column}"
            )

            relevant_tables.add(table_name)

    def _add_related_tables(
        self,
        schema,
        relevant_tables
    ):
        """
        Add tables connected through foreign-key relationships.

        This prevents the pruner from removing tables that may be
        required for SQL JOIN operations.
        """

        expanded_tables = set(relevant_tables)

        changed = True

        while changed:

            changed = False

            for fk in schema["foreign_keys"]:

                from_table = fk["from_table"]
                to_table = fk["to_table"]

                if (
                    from_table in expanded_tables
                    and
                    to_table not in expanded_tables
                ):

                    expanded_tables.add(to_table)
                    changed = True

                elif (
                    to_table in expanded_tables
                    and
                    from_table not in expanded_tables
                ):

                    expanded_tables.add(from_table)
                    changed = True

        return expanded_tables
#schema_pruner