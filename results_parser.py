from datetime import datetime
from typing import List


class ReportMetrics:
    def __init__(self, date: str):
        self.date = date
        self.metrics = {}


def parse(report: str, metrics: List[str]) -> ReportMetrics:
    if report is None:
        return None

    split = report.split("----------------------------------------------------------\n")

    metrics_split = split[2].split("\n")
    date = convert_to_desired_format(split[1].split("Run at ")[1].split("\n")[0])

    report_metrics = ReportMetrics(date=date)

    try:
        for line in metrics_split:
            for metric in metrics:

                if line.startswith(metric):
                    values = line.split(":")
                    report_metrics.metrics[metric] = float(values[1].split()[1])
    except IndexError:
        return None

    return report_metrics


def convert_to_desired_format(date_str):
    # Define the input and output date formats
    input_format = "%a %b %d %H:%M:%S UTC %Y"
    output_format = "%Y-%m-%d"

    try:
        parsed_date = datetime.strptime(date_str, input_format)
        formatted_date = parsed_date.strftime(output_format)
        return formatted_date
    except ValueError:
        print("Invalid date format")
        return None
