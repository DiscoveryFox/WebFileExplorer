import os
import shutil
import tempfile


class TempManager:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def del_from_tmpdir(self, file_name: str):
        current_dir = os.getcwd()
        os.chdir(self.temp_dir)
        os.remove(file_name)
        os.chdir(current_dir)

    # todo: write handlers for all errors that can occur on file operations

    def save_to_tmpdir(self, file_name: str):
        full_path = os.path.abspath(file_name)
        if os.path.isfile(full_path):
            try:
                shutil.copy(full_path, f'{self.temp_dir}/{file_name}')
            except FileNotFoundError:
                return True, 'File not found'
            except PermissionError:
                return True, 'PermissionError on rename'
            return False, ''
        elif os.path.isdir(full_path):
            try:
                shutil.copytree(full_path, f'{self.temp_dir}/{file_name}')
            except FileNotFoundError:
                return True, 'File not found'
            except PermissionError:
                return True, 'PermissionError on rename'
            return False, ''
