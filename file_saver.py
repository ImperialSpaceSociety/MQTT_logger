from pathlib import Path

data_dump_location = Path("datadump/")


class FileSaver:
    def __init__(self):
        pass

    @staticmethod
    def save_file(filename: str, content: bytes):
        data_dump_location.mkdir(parents=True, exist_ok=True)
        filepath = data_dump_location / filename
        filepath.write_bytes(content)
