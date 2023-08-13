import unittest

from single_file_cache import SingleFileCache


class SingleFileCacheTestCase(unittest.TestCase):
    def test_single_file_add(self):
        cache = SingleFileCache("test-cache")
        cache.add_to_cache("test", "value")

        self.assertEqual("value", cache.retrieve_value("test"))
        self.assertEqual(None, cache.retrieve_value("test2"))

        cache.delete_cache()

    def test_single_file_does_not_exist_returns_none(self):
        cache = SingleFileCache("test-cache")
        self.assertEqual(None, cache.retrieve_value("test"))
        cache.delete_cache()

