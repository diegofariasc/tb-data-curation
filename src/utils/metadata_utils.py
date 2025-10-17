import hashlib
import json
import datetime
import os


def hash_file(filepath: str):
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def log_metadata(source_name: str, file_path: str, rows: int, file_hash: str):
    os.makedirs("docs", exist_ok=True)
    metadata_path = "docs/metadata.json"
    entry = {
        "source": source_name,
        "file": os.path.basename(file_path),
        "rows": rows,
        "hash": file_hash,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(metadata_path, "w") as f:
        json.dump(data, f, indent=2)
