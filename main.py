from collections import defaultdict
from typing import List
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


from file_cache import FileCache
from github_client import GithubClient

COMMIT_CACHE_FILE = 'cache/date-commit-cache.json'
REPO_CACHE_FILE = 'cache/repo-cache.json'

EXTENSIONS = [
    ".java",
    ".groovy"
]


def count_by_file_type(files: List[str]) -> dict:
    file_counts = defaultdict(int)
    for file in files:
        for ext in EXTENSIONS:
            if file.endswith(ext):
                file_counts[ext] += 1
    return file_counts


def get_commit_by_date(gh_client: GithubClient, cache: FileCache, repository, date):
    find_commit = cache.retrieve_value(date)
    if not find_commit:
        find_commit = gh_client.get_most_recent_commit(repository, date)
        if find_commit:
            cache.add_to_cache(date, find_commit)

    return find_commit


def get_repository_by_commit(gh_client: GithubClient, cache: FileCache, repository, commit):
    find_repo = cache.retrieve_value(commit)

    if not find_repo:
        find_repo = gh_client.get_repository_at_commit(repository, commit)
        cache.add_to_cache(commit, find_repo)

    return find_repo


def get_dates_since(date_str):
    date_format = "%Y-%m-%d"
    output_format = "%Y-%m-%dT%H:%M:%SZ"

    # Parse the input date string
    start_date = datetime.strptime(date_str, date_format).date()

    # Get the current date
    end_date = datetime.now().date()

    # Calculate the difference in days
    days_diff = (end_date - start_date).days

    # Generate the list of dates
    date_list = []
    for i in range(0, days_diff + 1, 14):
        date_item = start_date + timedelta(days=i)
        date_str = date_item.strftime(output_format)
        date_list.append(date_str)

    return date_list


if __name__ == '__main__':
    print("starting")
    repo = "open-telemetry/opentelemetry-java-instrumentation"

    client = GithubClient()

    commit_cache = FileCache(COMMIT_CACHE_FILE)
    repo_cache = FileCache(REPO_CACHE_FILE)

    timeframe = get_dates_since("2022-11-15")
    result = defaultdict(dict)

    for snapshot in timeframe:
        try:
            commit = get_commit_by_date(gh_client=client, cache=commit_cache, date=snapshot, repository=repo)
            repo_files = get_repository_by_commit(gh_client=client, cache=repo_cache, repository=repo, commit=commit)
            count = count_by_file_type(repo_files["files"])
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
