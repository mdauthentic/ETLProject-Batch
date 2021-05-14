import json
import pathlib
import logging
from typing import Any, Dict, List


def get_path(dir: str, source: str = "") -> pathlib.Path:
    if not source:
        return pathlib.Path(__file__).parent.absolute() / dir
    return pathlib.Path(__file__).parent.absolute() / dir / source


def write_json(dir: str, source: str, data: List[Dict[str, Any]]) -> None:
    fpath = get_path(dir, source)
    with open(fpath, "w") as fout:
        json.dump(data, fout)
        logging.info("Data successfully written to file")


def read_json(dir: str) -> List[Dict[str, Any]]:
    with open(dir) as f:
        data = json.load(f)
        return data


def delete_local_dir(trash_dir):
    try:
        pathlib.Path.rmdir(trash_dir)
    except OSError as e:
        print(f"Error {trash_dir} : {e.strerror}")
