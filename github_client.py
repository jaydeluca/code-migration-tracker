import requests
import os

EXTENSIONS = [
    ".java",
    ".groovy"
]


def matches_extensions(path: str):
    for ext in EXTENSIONS:
        if path.endswith(ext):
            return True
    return False


def matches_directory(path: str):
    return path.startswith("instrumentation/")


def matches_meta(item):
    return item["type"] == "blob" and "test" in item["path"]


def parse_data(payload):
    data_result = []
    tree = payload["tree"]
    for i in tree:
        if matches_meta(i) and matches_extensions(i["path"]) and matches_directory(i["path"]):
            data_result.append(i["path"])

    json_result = {
        "files": data_result
    }
    return json_result


class GithubClient(object):

    def __init__(self):
        token = os.environ.get("GITHUB_TOKEN")
        self.session = requests.Session()
        if len(token):
            self.session.headers.update({'Authorization': f'Bearer {token}'})
        self.base_url = 'https://api.github.com'

    def _get(self, url, params=None):
        try:
            return self.session.get(url, params=params)
        except Exception as e:
            print(e)

    def get_most_recent_commit(self, repo, timestamp) -> requests.models.Response:
        api_url = f"{self.base_url}/repos/{repo}/commits"

        params = {
            "per_page": 1,
            "until": timestamp,
            "order": "desc"
        }

        response = self._get(api_url, params=params)

        if response.status_code == 200:
            commits = response.json()
            if len(commits) > 0:
                most_recent_commit = commits[0]
                return most_recent_commit['sha']
            else:
                print("No commits found.")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_repository_at_commit(self, repository, commit_sha):
        api_url = f"{self.base_url}/repos/{repository}/git/trees/{commit_sha}?recursive=1"

        response = self._get(api_url)

        if response.status_code == 200:
            return parse_data(response.json())
        else:
            print(f"Error: {response.status_code}")
            return None

