from src.logger import get_logger

logger = get_logger(__name__)

class SchemaExtractor:

    def __init__(self, tables_data):
        self.tables_data = tables_data

    def get_schema(self, db_id):

        for db in self.tables_data:

            if db["db_id"] == db_id:

                schema = {
                    "database": db_id,
                    "tables": {},
                    "primary_keys": [],
                    "foreign_keys": []
                }

                table_names = db["table_names_original"]
                column_names = db["column_names_original"]

                # ----------------------------
                # Extract Tables + Columns
                # ----------------------------
                for table_index, table_name in enumerate(table_names):

                    schema["tables"][table_name] = []

                    for col_table_id, col_name in column_names:

                        if col_table_id == table_index:

                            schema["tables"][table_name].append(col_name)

                logger.debug(f"Tables: {schema['tables']}")
                # ----------------------------
                # Primary Keys
                # ----------------------------
                for pk in db["primary_keys"]:

                    table_id, column_name = column_names[pk]

                    schema["primary_keys"].append({
                        "table": table_names[table_id],
                        "column": column_name
                    })
                logger.debug(f"Primary Keys: {schema['primary_keys']}")
                # ----------------------------
                # Foreign Keys
                # ----------------------------
                for source, target in db["foreign_keys"]:

                    source_table, source_column = column_names[source]

                    target_table, target_column = column_names[target]

                    schema["foreign_keys"].append({
                        "from_table": table_names[source_table],
                        "from_column": source_column,
                        "to_table": table_names[target_table],
                        "to_column": target_column
                    })
                    
                logger.debug(f"Foreign Keys: {schema['foreign_keys']}")

                schema["metadata"] = {

                    "db_id": db["db_id"],

                    "table_count": len(table_names),

                    # Spider includes one pseudo-column (*)
                    "column_count": len(column_names) - 1,

                    "primary_key_count": len(db["primary_keys"]),

                    "foreign_key_count": len(db["foreign_keys"])
                }

                
                return schema

        
        return None