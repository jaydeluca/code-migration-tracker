import unittest
import json

from data_filter import DataFilter


class ParseDataTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.file_extensions = [
            ".java",
            ".groovy"
        ]
        super(ParseDataTestCase, self).__init__(*args, **kwargs)

    def test_filters_payload_to_expected_files_based_on_criteria(self):
        with open("test_mocks/tree_data.json", 'r') as file:
            data = json.load(file)

            data_filter = DataFilter(file_extensions=self.file_extensions, path_prefix="instrumentation/", keyword="test")

            test = data_filter.parse_data(payload=data)

            expects = set()
            expects.add("instrumentation/src/main/java/instrumentation/TestFailableCallable.java")
            expects.add("instrumentation/src/main/java/instrumentation/TestInstrumentationModule.java")
            self.assertEqual(set(test['files']), expects)

    def test_given_url_with_different_case_than_keyword_still_filters_correctly(self):
        payload = """
        {
            "sha": "1e9b47b4c35f9046cec3718cadbc7410fdd9ffe1",
            "url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/trees/1e9b47b4c35f9046cec3718cadbc7410fdd9ffe1",
            "tree": [
                {
                    "type": "blob",
                    "path": "instrumentation/src/main/java/instrumentation/TestFailableCallable.java"
                }
            ]
        }
        """
        data = json.loads(payload)

        data_filter = DataFilter(file_extensions=self.file_extensions, path_prefix="instrumentation/", keyword="test")

        test = data_filter.parse_data(payload=data)

        expects = ["instrumentation/src/main/java/instrumentation/TestFailableCallable.java"]
        self.assertEqual(expects, test['files'])

