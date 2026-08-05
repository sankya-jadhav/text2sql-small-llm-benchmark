import sqlite3
import time

from src.models import ExecutionResult


class SQLExecutor:

    def execute(self, database_path, sql):

        start = time.perf_counter()

        try:

            connection = sqlite3.connect(database_path)

            cursor = connection.cursor()

            cursor.execute(sql)

            rows = cursor.fetchall()

            connection.close()

            elapsed = time.perf_counter() - start

            return ExecutionResult(

                success=True,

                rows=rows,

                execution_time=elapsed

            )

        except Exception as e:

            elapsed = time.perf_counter() - start

            return ExecutionResult(

                success=False,

                rows=[],

                execution_time=elapsed,

                error=str(e)

            )