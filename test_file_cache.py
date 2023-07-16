import unittest

from file_cache import FileCache


class FileCacheTestCase(unittest.TestCase):
    def test_add(self):
        cache = FileCache("test-cache")
        cache.add_to_cache("test", "value")

        self.assertEqual("value", cache.retrieve_value("test"))
        self.assertEqual(None, cache.retrieve_value("test2"))

        cache.delete_cache()

    def test_does_not_exist_returns_none(self):
        cache = FileCache("test-cache")
        self.assertEqual(None, cache.retrieve_value("test"))
        cache.delete_cache()

