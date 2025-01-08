import unittest

from instrumentation_analysis import analyze_instrumentation, parse_readme


class TestInstrumentationAnalysis(unittest.TestCase):
    def test_parse_file_list(self):
        file_list = [
            "akka/akka-actor-2.3/javaagent",
            "akka/akka-actor-fork-join-2.5/library"
        ]

        result = analyze_instrumentation(file_list)

        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].name, "akka-actor-2.3")
        self.assertEqual(result[0].has_javaagent, True)
        self.assertEqual(result[0].has_library, False)
        self.assertEqual(result[0].parent, "akka")

        self.assertEqual(result[1].name, "akka-actor-fork-join-2.5")
        self.assertEqual(result[1].has_javaagent, False)
        self.assertEqual(result[1].has_library, True)
        self.assertEqual(result[1].parent, "akka")

    def test_parse_file_list_with_two_layers(self):
        file_list = [
            "spring/spring-webmvc/spring-webmvc-5.3/library",
        ]

        result = analyze_instrumentation(file_list)

        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].name, "spring-webmvc-5.3")
        self.assertEqual(result[0].has_javaagent, False)
        self.assertEqual(result[0].has_library, True)
        self.assertEqual(result[0].parent, "spring/spring-webmvc")

    def test_parse_readme(self):
        input = [
            'spring/spring-webmvc/spring-webmvc-5.3/library/README.md',
            'aws-lambda/aws-lambda-core-1.0/javaagent/README.md',
            'ktor/ktor-1.0/library/README.md',
            'java-http-client/library/README.md'
        ]

        javaagents_with_readmes, libraries_with_readmes = parse_readme(input)


        self.assertIn('aws-lambda-core-1.0', javaagents_with_readmes)
        self.assertIn('spring-webmvc-5.3', libraries_with_readmes)
        self.assertIn('ktor-1.0', libraries_with_readmes)
        self.assertIn('java-http-client', libraries_with_readmes)
