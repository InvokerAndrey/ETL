import os
from pathlib import Path


class State:
    """
        Класс для хранения состояния при работе с данными,
        чтобы постоянно не перечитывать данные с начала.
    """
    def __init__(self, file_name: str):
        self.storage_file = os.path.join(Path(__file__).resolve().parent, file_name)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def set_state(self, value: int):
        with open(self.storage_file, 'w') as f:
            f.write(str(value))

    def get_state(self):
        try:
            with open(self.storage_file, 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            open(self.storage_file, 'w').close()
            return None
        except ValueError:
            return None

    def clear_state(self):
        open(self.storage_file, 'w').close()
