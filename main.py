from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import argparse
from utilities import count_by_file_extension, get_dates_between

from single_file_cache import SingleFileCache
from github_client import GithubClient

COMMIT_CACHE_FILE = 'cache/date-commit-cache.json'
REPO_CACHE_FILE = 'cache/repo-cache.json'


def get_commit_by_date(gh_client: GithubClient, cache: SingleFileCache, repository, date):
    find_commit = cache.retrieve_value(date)
    if not find_commit:
        find_commit = gh_client.get_most_recent_commit(repository, date)
        if find_commit:
            cache.add_to_cache(date, find_commit)

    return find_commit


def get_repository_by_commit(gh_client: GithubClient, cache: SingleFileCache, repository,
                             commit):
    find_repo = cache.retrieve_value(commit)

    if not find_repo:
        find_repo = gh_client.get_repository_at_commit(repository, commit)
        cache.add_to_cache(commit, find_repo)

    return find_repo


def main(args):
    client = GithubClient()

    file_extensions = [
        ".java",
        ".groovy"
    ]

    commit_cache = SingleFileCache(COMMIT_CACHE_FILE)
    repo_cache = SingleFileCache(REPO_CACHE_FILE)

    timeframe = get_dates_between(args.start, datetime.now().date(), args.interval)
    result = defaultdict(dict)

    for snapshot in timeframe:
        try:
            commit = get_commit_by_date(gh_client=client, cache=commit_cache,
                                        date=snapshot, repository=args.repo)
            repo_files = get_repository_by_commit(
                gh_client=client,
                cache=repo_cache,
                repository=args.repo,
                commit=commit
            )
            count = count_by_file_extension(files=repo_files["files"],
                                            file_extensions=file_extensions)
            if count:
                result[snapshot] = {
                    "date": snapshot,
                    "java": count[".java"],
                    "groovy": count[".groovy"]
                }
        except Exception as e:
            print(f"Error for {snapshot}, {e}")

    dates = []
    java_counts = []
    groovy_counts = []

    for item in result.values():
        date = item["date"][:10]
        java_count = item["java"]
        groovy_count = item["groovy"]
        dates.append(date)
        java_counts.append(java_count)
        groovy_counts.append(groovy_count)

    plt.plot(dates, java_counts, label='Java')
    plt.plot(dates, groovy_counts, label='Groovy')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Test Classes by Lang in Instrumentation Directory')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
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
    arguments = parser.parse_args()
    main(arguments)
