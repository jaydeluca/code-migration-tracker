from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict

from CodeFile import CodeFile


def get_dates_between(start_date_str, end_date, interval):
    date_format = "%Y-%m-%d"
    output_format = "%Y-%m-%dT%H:%M:%SZ"

    # Parse the input date string
    start_date = datetime.strptime(start_date_str, date_format).date()

    # Convert end date to date if string
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Calculate the difference in days
    days_diff = (end_date - start_date).days

    # Generate the list of dates
    date_list = set()
    for i in range(0, days_diff + 1, int(interval)):
        date_item = start_date + timedelta(days=i)
        start_date_str = date_item.strftime(output_format)
        date_list.add(start_date_str)

    # include end of today in the set if end_date is today
    if end_date == datetime.now().date():
        date_list.add((datetime.now() + timedelta(days=1)).strftime(output_format))

    return date_list


def count_by_file_extension(files: List[str], languages: List[str]) -> dict:
    file_counts = defaultdict(int)
    for file in files:
        for ext in languages:
            extension = f".{ext.lower()}"
            if file.endswith(extension) and "grails" not in file:
                file_counts[ext] += 1
    return file_counts


@dataclass
class FileCountInfo:
    file_counts: Dict[str, int]
    file_sizes: Dict[str, int]
    matched_files: List[CodeFile]


def count_by_language_and_file_extension(files: List[CodeFile], languages: List[str]) -> FileCountInfo:
    matched_files = []
    file_counts = defaultdict(int)
    file_sizes = defaultdict(int)
    for file in files:
        file_parts = file.path.split('/')
        if len(file_parts) < 3:
            continue
        instrumentation = file_parts[1]
        extension = file_parts[-1].split('.')[-1]
        if extension in languages:
            file_counts[instrumentation] += 1
            file_sizes[instrumentation] += file.size
            matched_files.append(file.path)
    return FileCountInfo(file_counts=file_counts, file_sizes=file_sizes,
                         matched_files=matched_files)


def convert_to_plot(input_dict: dict, items):
    result = {}
    dates = []
    for entry in input_dict.values():
        dates.append(entry["date"][:10])
        for item in items:
            try:
                result[item].append(entry[item])
            except KeyError:
                result[item] = [entry[item]]
    return dates, result
