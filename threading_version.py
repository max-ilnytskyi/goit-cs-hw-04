from threading import Thread, RLock
import time
from typing import List
import logging

from common import (
    search_keyword_in_file,
    get_file_paths,
    split_file_paths,
    DIRECTORY,
    KEYWORD,
    MAX_THREADS_AMOUNT,
)


def thread_worker(file_paths: List[str], keyword, result: List[str], lock: RLock):
    logging.debug("Run")
    for file_path in file_paths:
        has_word = search_keyword_in_file(file_path, keyword)
        if has_word:
            with lock:
                result.append(file_path)


def threading_approach(directory, keywords) -> List[str]:
    file_paths = None
    file_paths = get_file_paths(directory)

    threads: List[Thread] = []
    result: List[str] = []
    threads_amount: int = min(len(file_paths), MAX_THREADS_AMOUNT)

    lock = RLock()

    file_paths_by_thread = split_file_paths(file_paths, threads_amount)

    start_time = time.time()
    for index in range(0, threads_amount):
        thread = Thread(
            target=thread_worker,
            args=(file_paths_by_thread[index], keywords, result, lock),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threading approach took {end_time - start_time:.6f} seconds.")
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    file_paths = get_file_paths(DIRECTORY)

    print("Starting threading approach...")

    threading_result = threading_approach(DIRECTORY, KEYWORD)

    print("Threading Results:")
    if len(threading_result) == 0:
        print("No files found")
    else:
        print("\n".join(threading_result))
