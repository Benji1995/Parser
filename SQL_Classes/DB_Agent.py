
from .DB_Init import DB_Init


class DB_Agent(DB_Init):
    def __init__(self) -> None:
        super().__init__()
        self.tables=self.json_data['used_tables']
        pass

