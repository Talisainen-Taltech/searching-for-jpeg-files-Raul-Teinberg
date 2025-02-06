import zipfile
from io import BytesIO
from pathlib import Path

import requests

# Declare parameters
script_path: Path = Path(__file__).parent

url: str = "https://upload.itcollege.ee/~aleksei/random_files_without_extension.zip"
files_dir: Path = script_path / "random_files"

# Remove the files directory if it already exists
if files_dir.exists():
    for entry in files_dir.iterdir():
        if entry.is_file():
            entry.unlink()
        else:
            entry.rmdir()
    files_dir.rmdir()

# Download the zip file and extract it directly from memory
with zipfile.ZipFile(
        BytesIO(
            requests.get(url).content
        )
    ) as zip_ref:
    zip_ref.extractall(script_path)

# Remove files that are not images
for entry in files_dir.iterdir():
    if entry.is_file() and entry.read_bytes()[:2] == b"\xff\xd8":
        entry.rename(entry.with_suffix(".jpeg"))
    else:
        entry.unlink()
