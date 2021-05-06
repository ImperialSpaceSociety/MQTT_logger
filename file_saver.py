from pathlib import Path

data_dump_location = Path("datadump/")
html_render_location = Path("renders/")

class FileSaver:
    def __init__(self):
        data_dump_location.mkdir(parents=True, exist_ok=True)
        html_render_location.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def save_file(filename: str, content: bytes):
        filepath = data_dump_location / filename
        filepath.write_bytes(content)
