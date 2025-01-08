import base64

import requests
import os


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

    def get_most_recent_commit(self, repo: str, timestamp: str, branch: str):
        api_url = f"{self.base_url}/repos/{repo}/commits"

        params = {
            "per_page": 1,
            "until": timestamp,
            "order": "desc",
            "sha": branch
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

    def get_repository_at_commit(self, repository: str, commit_sha: str):
        api_url = f"{self.base_url}/repos/{repository}/git/trees/{commit_sha}?recursive=1"

        response = self._get(api_url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_file_at_commit(self, repository: str, filepath: str, commit_sha: str):
        api_url = f"{self.base_url}/repos/{repository}/contents/{filepath}"

        response = self._get(api_url, params={"ref": commit_sha})

        if response.status_code == 200:
            # File content is base64 encoded, decode it
            content = response.json().get("content", "")
            content = base64.b64decode(content)
            return str(content, encoding='utf-8')
        else:
            print(f"Error: {response.status_code}")
            return None
