import os
from typing import List, Tuple


def find_string_in_files(file_list: List[str], search_string: str) -> List[str]:
    matching_files = []
    for file_path in file_list:
        if file_path.endswith(".java"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        if search_string in line:
                            matching_files.append(file_path)
                            break
            except FileNotFoundError:
                continue
    return matching_files


def traverse_and_search(root_dir: str, search_string: str) -> List[Tuple[str, str]]:
    matching_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        file_paths = [os.path.join(dirpath, f) for f in filenames]
        for file_path in find_string_in_files(file_paths, search_string):
            instrumentation_name = file_path.split("/instrumentation/")[1].split("/")[0]
            matching_files.append((instrumentation_name, file_path))
    return matching_files


if __name__ == "__main__":
    root_directory = "/Users/jay/code/projects/opentelemetry-java-instrumentation/instrumentation/"
    search_str = "DbClientMetrics.get()"
    result = traverse_and_search(root_directory, search_str)
    for instrumentation_name, file_path in result:
        print(f"{instrumentation_name}: {file_path}")
