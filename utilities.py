from datetime import datetime, timedelta
from collections import defaultdict
from typing import List


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
