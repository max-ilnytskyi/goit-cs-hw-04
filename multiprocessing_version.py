from multiprocessing import Process, Queue, current_process
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

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def process_worker(file_paths: List[str], keyword, result_queue: Queue):
    logger.debug(f"{current_process().name} Run")
    for file_path in file_paths:
        has_word = search_keyword_in_file(file_path, keyword)
        if has_word:
            result_queue.put(file_path)


def multiprocessing_approach(directory, keyword) -> List[str]:
    file_paths = get_file_paths(directory)

    processes: List[Process] = []
    result_queue = Queue()
    processes_amount: int = min(len(file_paths), MAX_THREADS_AMOUNT)

    file_paths_by_process = split_file_paths(file_paths, processes_amount)

    start_time = time.time()
    for index in range(0, processes_amount):
        process = Process(
            target=process_worker,
            args=(file_paths_by_process[index], keyword, result_queue),
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    result = []
    while not result_queue.empty():
        result.append(result_queue.get())

    end_time = time.time()
    print(f"Multiprocessing approach took {end_time - start_time:.6f} seconds.")
    return result


if __name__ == "__main__":
    print("Starting multiprocessing approach...")

    multiprocessing_result = multiprocessing_approach(DIRECTORY, KEYWORD)

    print("Multiprocessing Results:")
    if len(multiprocessing_result) == 0:
        print("No files found")
    else:
        print("\n".join(multiprocessing_result))
