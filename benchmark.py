import matplotlib.pyplot as plt
import argparse
from github_client import GithubClient
from results_parser import parse
from single_file_cache import SingleFileCache
from utilities import get_dates_between, convert_to_plot
from datetime import datetime
from collections import defaultdict

COMMIT_CACHE_FILE = 'cache/benchmark-date-commit-cache.json'
REPORT_CACHE_FILE = 'cache/benchmark-report-cache.json'


class BenchmarkApp:
    def __init__(self, file_path: str):
        self.client = GithubClient()
        self.commit_cache = SingleFileCache(location=COMMIT_CACHE_FILE)
        self.report_cache = SingleFileCache(location=REPORT_CACHE_FILE)
        self.file_path = file_path

    def get_commit_by_date(self, repository, date):
        find_commit = self.commit_cache.retrieve_value(date)
        if not find_commit:
            find_commit = self.client.get_most_recent_commit(repository, date, "gh-pages")
            if find_commit:
                self.commit_cache.add_to_cache(date, find_commit)

        return find_commit

    def get_report_by_commit(self, repository, commit):
        repo_data = self.report_cache.retrieve_value(commit)

        if not repo_data:
            repo_data = self.client.get_file_at_commit(repository=repository, filepath=self.file_path, commit_sha=commit)
            self.report_cache.add_to_cache(commit, repo_data)

        return repo_data


def main(args):
    file_path = "benchmark-overhead/results/release/summary.txt"

    metrics = [
        "Min heap used (MB)",
        "Max heap used (MB)"
    ]

    timeframe = get_dates_between(args.start, datetime.now().date(), args.interval)
    result = defaultdict(dict)

    app = BenchmarkApp(file_path=file_path)

    for snapshot in timeframe:
        commit = app.get_commit_by_date(date=snapshot, repository=args.repo)

        report = app.get_report_by_commit(repository=args.repo, commit=commit)
        parsed = parse(report, metrics)
        if parsed:
            result[snapshot]["date"] = snapshot
            for metric in metrics:
                result[snapshot][metric] = parsed.metrics[metric]

    dates, metric_values = convert_to_plot(result, metrics)

    for metric, values in metric_values.items():
        plt.plot(dates, values, label=metric)

    plt.xlabel('Date')
    plt.ylabel('MB')
    plt.title('Benchmark Metrics')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Benchmark Tracker')
    parser.add_argument("-r", "--repo",
                        help="Repository name. "
                             "ex: open-telemetry/opentelemetry-java-instrumentation",
                        required=True)
    parser.add_argument("-s", "--start",
                        help="Starting Date (will calculate from this date until now)",
                        required=True)
    parser.add_argument("-i", "--interval",
                        help="Interval (in days) between data points", required=True)
    arguments = parser.parse_args()
    main(arguments)
