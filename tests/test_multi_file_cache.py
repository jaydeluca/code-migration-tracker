import unittest
import os

from multi_file_cache import MultiFileCache


class MultiFileCacheTestCase(unittest.TestCase):
    def test_add_key_creates_new_file(self):
        cache = MultiFileCache("./cache/test-cache")
        cache.add_to_cache("testkey", "value")

        self.assertTrue(os.path.isfile('./cache/test-cache/testkey.json'))

        cache.delete_cache()
        self.assertFalse(os.path.isfile('./cache/test-cache/testkey.json'))

    def test_multi_file_does_not_exist_returns_none(self):
        cache = cache = MultiFileCache("./cache/test-cache")
        self.assertEqual(None, cache.retrieve_value("test"))
        cache.delete_cache()

