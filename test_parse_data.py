import unittest
import json

from github_client import parse_data


class ParseDataTestCase(unittest.TestCase):
    def test_clean_payload(self):
        with open("test_mocks/tree_data.json", 'r') as file:
            data = json.load(file)
            test = parse_data(data)

            expects = set()
            expects.add("instrumentation/internal/internal-class-loader/javaagent-integration-tests/src/main/java/instrumentation/TestFailableCallable.java")
            expects.add("instrumentation/internal/internal-class-loader/javaagent-integration-tests/src/main/java/instrumentation/TestInstrumentationModule.java")
            self.assertEqual(set(test['files']), expects)



