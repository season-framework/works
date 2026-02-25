import os
from season.util import filesystem

class FileSystem:
    def __init__(self, base_path="."):
        self.fs = filesystem(base_path)

    def read(self, path: str):
        if path.startswith("/"): _path = path
        else: _path = self.fs.abspath(path)
        try:
            with open(_path, 'r', encoding='utf-8') as file:
                return file.read()
        except: return None

    def write(self, path: str, text: str):
        if path.startswith("/"): _path = path
        else: _path = self.fs.abspath(path)
        try:
            with open(_path, 'w', encoding='utf-8') as file:
                file.write(text)
        except Exception as e:
            print(e)

    def exists(self, path: str):
        if path.startswith("/"):
            return os.path.exists(path)
        else:
            return self.fs.exists(path)

Model = FileSystem
