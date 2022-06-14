import os
import shutil
import tempfile
import platform


class TempManager:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def del_from_tmpdir(self, file_name: str):
        current_dir = os.getcwd()
        os.chdir(self.temp_dir)
        os.remove(file_name)
        os.chdir(current_dir)

    # todo: write handlers for all errors that can occur on file operations

    def save_to_tmpdir(self, file_name: str) -> tuple[bool, str]:
        """
        Saves a file to the temporary directory. And deletes it from the current directory.
        :param file_name: str
        :return: tuple[bool, str]
        """
        full_path = os.path.abspath(file_name)
        if os.path.isfile(full_path):
            try:
                print(platform.system())
                if platform.system() == 'Windows':
                    shutil.copy(full_path, f'{self.temp_dir}\\{file_name}')
                    print(f'{full_path} -> {self.temp_dir}\\{file_name}')
                else:
                    shutil.copy(full_path, f'{self.temp_dir}/{file_name}')
                    print(f'{full_path} -> {self.temp_dir}/{file_name}')
                os.remove(full_path)
            except FileNotFoundError:
                return True, 'File not found'
            except PermissionError:
                return True, 'PermissionError on rename'
            return False, ''
        elif os.path.isdir(full_path):
            try:
                shutil.copytree(full_path, f'{self.temp_dir}/{file_name}')
                shutil.rmtree(full_path)
            except FileNotFoundError:
                return True, 'File not found'
            except PermissionError:
                return True, 'PermissionError on rename'
            return False, ''

    def restore_from_tmpdir(self, file_name: str) -> tuple[bool, str]:
        """
        Restores a file from the temporary directory. And deletes it from the temporary directory.
        :param file_name: str
        :return: tuple[bool, str]
        """
        try:
            shutil.copy(f'{self.temp_dir}/{file_name}', os.getcwd())
            os.remove(f'{self.temp_dir}/{file_name}')
        except FileNotFoundError:
            return True, 'File not found'
        except PermissionError:
            return True, 'PermissionError on rename'
        return False, ''
