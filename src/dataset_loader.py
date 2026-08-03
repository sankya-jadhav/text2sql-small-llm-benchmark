import json


class DatasetLoader:

    def __init__(self, dev_path, tables_path):
        self.dev_path = dev_path
        self.tables_path = tables_path

        self.dev_data = None
        self.tables_data = None

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