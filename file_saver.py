from pathlib import Path

class FileSaver:
    def __init__(self):
        pass

    @staticmethod
    def save_file(filename: str, content : bytes):
        p = Path("datadump/")
        p.mkdir(parents=True, exist_ok=True)
        filepath = p / filename
        filepath.write_bytes(content)