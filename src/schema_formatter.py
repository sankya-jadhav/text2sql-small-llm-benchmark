class SchemaFormatter:

    def format(self, schema):

        lines = []

        lines.append(f"Database: {schema['database']}")
        lines.append("")

        lines.append("Tables")
        lines.append("")

        for table, columns in schema["tables"].items():

            lines.append(f"Table: {table}")

            for column in columns:
                lines.append(f"  - {column}")

            lines.append("")

        lines.append("Relationships")
        lines.append("")

        for fk in schema["foreign_keys"]:

            relation = (
                f"{fk['from_table']}.{fk['from_column']} "
                f"-> "
                f"{fk['to_table']}.{fk['to_column']}"
            )

            lines.append(relation)

        return "\n".join(lines)