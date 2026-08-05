from pathlib import Path


class DatabaseManager:
    """
    Handles locating and validating Spider SQLite databases.
    """

    def __init__(self, database_root: str):
        self.database_root = Path(database_root)

    def get_database_path(self, db_id: str) -> Path:
        """
        Returns the path to the SQLite database.
        """

        return self.database_root / db_id / f"{db_id}.sqlite"

    def database_exists(self, db_id: str) -> bool:
        """
        Checks whether the SQLite database exists.
        """

        return self.get_database_path(db_id).exists()

    def get_available_databases(self):
        """
        Returns all databases that are available locally.
        """

        return sorted(
            [
                folder.name
                for folder in self.database_root.iterdir()
                if folder.is_dir()
            ]
        )