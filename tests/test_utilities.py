from unittest import TestCase

from utilities import get_dates_between, count_by_file_extension
from datetime import datetime


class TestUtilities(TestCase):
    def test_get_dates_since(self):
        start = "2023-01-01"
        end_date = datetime.strptime("2023-01-30", '%Y-%m-%d').date()
        interval = 7
        expected = ['2023-01-01T00:00:00Z',
                    '2023-01-08T00:00:00Z',
                    '2023-01-15T00:00:00Z',
                    '2023-01-22T00:00:00Z',
                    '2023-01-29T00:00:00Z'
                    ]

        result = get_dates_between(start, end_date, interval)

        self.assertEqual(expected, result)

    def test_get_dates_between_given_end_date_as_string_converts_to_date(self):
        start = "2023-01-01"
        end_date = "2023-01-30"
        interval = 7
        expected = ['2023-01-01T00:00:00Z',
                    '2023-01-08T00:00:00Z',
                    '2023-01-15T00:00:00Z',
                    '2023-01-22T00:00:00Z',
                    '2023-01-29T00:00:00Z'
                    ]

        result = get_dates_between(start, end_date, interval)

        self.assertEqual(expected, result)

    def test_count_by_file_extension(self):
        files = [
            "test1.java",
            "test2.java",
            "test3.java",
            "test4.groovy",
            "test5.groovy",
            "test6.txt"
        ]

        extensions = [
            ".java",
            ".groovy",
            ".txt"
        ]

        result = count_by_file_extension(files, extensions)
        self.assertEqual(3, result['.java'])
        self.assertEqual(2, result['.groovy'])
        self.assertEqual(1, result['.txt'])

