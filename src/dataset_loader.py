import json


class DatasetLoader:

    def __init__(self, dev_path, tables_path):
        self.dev_path = dev_path
        self.tables_path = tables_path

        self.dev_data = []
        self.tables_data = []

        self.load()

    def load(self):

        with open(self.dev_path, "r", encoding="utf-8") as f:
            self.dev_data = json.load(f)

        with open(self.tables_path, "r", encoding="utf-8") as f:
            self.tables_data = json.load(f)

    def get_question(self, index):
        return self.dev_data[index]

    def total_questions(self):
        return len(self.dev_data)

    def total_databases(self):
        return len(self.tables_data)
    def get_statistics(self):
        return {
            "questions": self.total_questions(),
            "databases": self.total_databases()
        }
    def get_available_questions(self, available_databases):

        return [

            question

            for question in self.dev_data

            if question["db_id"] in available_databases

        ]