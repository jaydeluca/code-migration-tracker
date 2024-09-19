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
    date_list = []
    for i in range(0, days_diff + 1, int(interval)):
        date_item = start_date + timedelta(days=i)
        start_date_str = date_item.strftime(output_format)
        date_list.append(start_date_str)

    return date_list


def count_by_file_extension(files: List[str], languages: List[str]) -> dict:
    file_counts = defaultdict(int)
    for file in files:
        for ext in languages:
            extension = f".{ext.lower()}"
            if file.endswith(extension):
                file_counts[ext] += 1
    return file_counts


def count_by_language_and_file_extension(files: List[CodeFile], languages: List[str]) -> Dict[str, Dict[str, int]]:
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
    return file_counts, file_sizes


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
