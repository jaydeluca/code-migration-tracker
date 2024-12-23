import unittest
from unittest.mock import Mock
from datetime import datetime
import pandas as pd

from count_by_instrumentation import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock().return_value
        self.mock_client.get_most_recent_commit.return_value = "dummy_commit"

        mock_repo_data = {"files": ["file1.java", "file2.groovy"]}
        self.mock_client.get_repository_at_commit.return_value = mock_repo_data

        self.languages = ["java", "groovy"]
        self.path_prefix = "instrumentation/"
        self.keyword = "test"
        self.app = App(languages=self.languages, path_prefix=self.path_prefix,
                       keyword=self.keyword, client=self.mock_client)
        self.repo = "open-telemetry/opentelemetry-java-instrumentation"
        self.commit = "dummy_commit"

    def test_get_commit_by_date(self):
        date = (datetime.now().date() + pd.Timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        result = self.app.get_commit_by_date(repository=self.repo, date=date)

        self.assertEqual(result, "dummy_commit")
        self.mock_client.get_most_recent_commit.assert_called_once_with(self.repo, date, "main")

