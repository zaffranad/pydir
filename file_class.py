from typing import List


class FileByExtension:
    def __init__(self, files: List[str]):
        self.files = files

    def count(self):
        return len(self.files)
