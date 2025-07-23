from datetime import datetime
import json
import os


class MemoryManager:
    def __init__(self):
        self.filepath = "data/test.json"
        self.keep_entries = 10
        self.check_file()

    def check_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)

    def get_data(self):
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    def save_data(self, data):
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def set_data(self, name, question):
        data = self.get_data()

        new_data = {
            "이름": name,
            "내용": question,
            "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        data.append(new_data)

        self.save_data(data)
