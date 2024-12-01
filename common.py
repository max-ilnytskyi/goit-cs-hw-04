import os
from typing import List

DIRECTORY = "files"
KEYWORD = "example"
MAX_THREADS_AMOUNT = 4


def get_file_paths(directory: str) -> List[str]:
    file_paths = []

    try:
        for root, _, files in os.walk(directory):
            for file in files:
                file_paths.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")

    return file_paths


def search_keyword_in_file(file_path: str, keyword: str) -> bool:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return keyword in content

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False


def split_file_paths(file_paths: List[str], threads_amount: int) -> List[List[str]]:
    result = [[] for _ in range(threads_amount)]
    for i, file_path in enumerate(file_paths):
        result[i % threads_amount].append(file_path)
    return result
