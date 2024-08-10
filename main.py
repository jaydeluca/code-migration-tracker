from collections import defaultdict
from datetime import datetime
from typing import List
import seaborn as sns
import pandas as pd

import matplotlib.pyplot as plt
import argparse

from data_filter import DataFilter
from multi_file_cache import MultiFileCache
from utilities import count_by_file_extension, get_dates_between, convert_to_plot

from single_file_cache import SingleFileCache
from github_client import GithubClient

COMMIT_CACHE_FILE = 'cache/date-commit-cache.json'
REPO_CACHE_FILE = 'cache/repo-cache'


class App:
    def __init__(self, languages: List[str], path_prefix: str, keyword: str):
        self.client = GithubClient()
        self.data_filter = DataFilter(languages=languages,
                                      path_prefix=path_prefix, keyword=keyword)
        self.commit_cache = SingleFileCache(location=COMMIT_CACHE_FILE)
        self.repo_cache = MultiFileCache(location=REPO_CACHE_FILE)

    def get_commit_by_date(self, repository, date):
        find_commit = self.commit_cache.retrieve_value(date)
        if not find_commit:
            find_commit = self.client.get_most_recent_commit(repository, date, "main")
            if find_commit:
                self.commit_cache.add_to_cache(date, find_commit)

        return find_commit

    def get_repository_by_commit(self, repository, commit):
        repo_data = self.repo_cache.retrieve_value(commit)

        if not repo_data:
            repo_data = self.client.get_repository_at_commit(repository, commit)
            repo_data = self.data_filter.parse_data(repo_data)
            self.repo_cache.add_to_cache(commit, repo_data)

        return repo_data


def main(args):
    languages = args.languages.split(",")

    app = App(
        languages=languages,
        path_prefix="instrumentation/",
        keyword="test"
    )

    timeframe = get_dates_between(args.start, datetime.now().date(), args.interval)
    result = defaultdict(dict)

    for snapshot in timeframe:
        try:
            commit = app.get_commit_by_date(date=snapshot, repository=args.repo)
            repo_files = app.get_repository_by_commit(
                repository=args.repo,
                commit=commit
            )
            count = count_by_file_extension(files=repo_files["files"],
                                            languages=languages)
            if count:
                result[snapshot]["date"] = snapshot
                for language in languages:
                    result[snapshot][language] = count[language]
        except Exception as e:
            print(f"Error for {snapshot}, {e}")

    dates, language_counts = convert_to_plot(result, languages)

    for item in result.values():
        dates.append(item["date"][:10])
        for language in languages:
            try:
                language_counts[language].append(item[language])
            except KeyError:
                language_counts[language] = [item[language]]

    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 8))

    for lang, counts in language_counts.items():
        df = pd.DataFrame({'Date': dates, 'Count': counts})
        df['Date'] = pd.to_datetime(df['Date'])
        sns.lineplot(x='Date', y='Count', label=lang.capitalize(), data=df, marker='o')

        # Find highest and lowest points
        highest_point = df[df['Count'] == df['Count'].max()]
        lowest_point = df[df['Count'] == df['Count'].min()]

        # Annotate the highest point
        plt.annotate(highest_point["Count"].values[0],
                     xy=(
                     highest_point['Date'].values[0], highest_point['Count'].values[0]),
                     xytext=(highest_point['Date'].values[0],
                             highest_point['Count'].values[0] - 40),
                     xycoords='data',
                     textcoords='data',
                     size=15, va="bottom", ha="left",
                     arrowprops=dict(arrowstyle="simple",
                                     connectionstyle="arc3,rad=-0.2"))

        # Annotate lowest point
        plt.annotate(lowest_point["Count"].values[0],
                     xy=(
                     lowest_point['Date'].values[0], lowest_point['Count'].values[0]),
                     xytext=(lowest_point['Date'].values[0],
                             lowest_point['Count'].values[0] + 40),
                     xycoords='data',
                     textcoords='data',
                     size=15, va="top", ha="left",
                     arrowprops=dict(arrowstyle="simple",
                                     connectionstyle="arc3,rad=-0.2"))

    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.title('Test File Count in Instrumentation Directory', fontsize=16)
    plt.xticks(rotation=45)

    plt.legend()
    plt.tight_layout()

    if args.output is not None:
        plt.savefig(args.output)
    else:
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Migration Tracker')
    parser.add_argument("-r", "--repo",
                        help="Repository name. "
                             "ex: open-telemetry/opentelemetry-java-instrumentation",
                        required=True)
    parser.add_argument("-s", "--start",
                        help="Starting Date (will calculate from this date until now)",
                        required=True)
    parser.add_argument("-i", "--interval",
                        help="Interval (in days) between data points", required=True)
    parser.add_argument("-l", "--languages",
                        help="Languages (comma separated list, no spaces)."
                             "ex: groovy,java",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="File name to output graph to (leave blank and no file is generated)."
                             "ex: file-count.png")
    arguments = parser.parse_args()
    main(arguments)
