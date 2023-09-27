from unittest import TestCase

from utilities import get_dates_between, count_by_file_extension, convert_to_plot
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

        languages = [
            "java",
            "groovy",
            "txt"
        ]

        result = count_by_file_extension(files, languages)
        self.assertEqual(3, result['java'])
        self.assertEqual(2, result['groovy'])
        self.assertEqual(1, result['txt'])

    def test_report_generator(self):
        metrics = [
            "Min heap used (MB)",
            "Max heap used (MB)"
        ]

        expected_dates = ['2022-11-16', '2022-11-30', '2022-12-14', '2022-12-28',
                          '2023-01-11', '2023-01-25', '2023-02-08', '2023-02-22',
                          '2023-03-08', '2023-03-22', '2023-04-05', '2023-04-19',
                          '2023-05-03', '2023-05-17', '2023-05-31', '2023-06-14',
                          '2023-06-28', '2023-07-12', '2023-07-26', '2023-08-09',
                          '2023-08-23', '2023-09-06', '2023-09-20']

        test = {'2022-11-16T00:00:00Z': {'date': '2022-11-16T00:00:00Z',
                                         'Min heap used (MB)': 88.37,
                                         'Max heap used (MB)': 360.79},
                '2022-11-30T00:00:00Z': {'date': '2022-11-30T00:00:00Z',
                                         'Min heap used (MB)': 93.24,
                                         'Max heap used (MB)': 357.57},
                '2022-12-14T00:00:00Z': {'date': '2022-12-14T00:00:00Z',
                                         'Min heap used (MB)': 93.12,
                                         'Max heap used (MB)': 489.0},
                '2022-12-28T00:00:00Z': {'date': '2022-12-28T00:00:00Z',
                                         'Min heap used (MB)': 93.36,
                                         'Max heap used (MB)': 339.98},
                '2023-01-11T00:00:00Z': {'date': '2023-01-11T00:00:00Z',
                                         'Min heap used (MB)': 90.34,
                                         'Max heap used (MB)': 448.27},
                '2023-01-25T00:00:00Z': {'date': '2023-01-25T00:00:00Z',
                                         'Min heap used (MB)': 90.57,
                                         'Max heap used (MB)': 343.99},
                '2023-02-08T00:00:00Z': {'date': '2023-02-08T00:00:00Z',
                                         'Min heap used (MB)': 88.31,
                                         'Max heap used (MB)': 389.67},
                '2023-02-22T00:00:00Z': {'date': '2023-02-22T00:00:00Z',
                                         'Min heap used (MB)': 89.99,
                                         'Max heap used (MB)': 334.34},
                '2023-03-08T00:00:00Z': {'date': '2023-03-08T00:00:00Z',
                                         'Min heap used (MB)': 85.4,
                                         'Max heap used (MB)': 340.25},
                '2023-03-22T00:00:00Z': {'date': '2023-03-22T00:00:00Z',
                                         'Min heap used (MB)': 94.67,
                                         'Max heap used (MB)': 362.89},
                '2023-04-05T00:00:00Z': {'date': '2023-04-05T00:00:00Z',
                                         'Min heap used (MB)': 83.31,
                                         'Max heap used (MB)': 406.11},
                '2023-04-19T00:00:00Z': {'date': '2023-04-19T00:00:00Z',
                                         'Min heap used (MB)': 108.68,
                                         'Max heap used (MB)': 474.59},
                '2023-05-03T00:00:00Z': {'date': '2023-05-03T00:00:00Z',
                                         'Min heap used (MB)': 90.29,
                                         'Max heap used (MB)': 396.23},
                '2023-05-17T00:00:00Z': {'date': '2023-05-17T00:00:00Z',
                                         'Min heap used (MB)': 96.5,
                                         'Max heap used (MB)': 448.06},
                '2023-05-31T00:00:00Z': {'date': '2023-05-31T00:00:00Z',
                                         'Min heap used (MB)': 94.72,
                                         'Max heap used (MB)': 362.23},
                '2023-06-14T00:00:00Z': {'date': '2023-06-14T00:00:00Z',
                                         'Min heap used (MB)': 112.4,
                                         'Max heap used (MB)': 483.55},
                '2023-06-28T00:00:00Z': {'date': '2023-06-28T00:00:00Z',
                                         'Min heap used (MB)': 109.7,
                                         'Max heap used (MB)': 478.83},
                '2023-07-12T00:00:00Z': {'date': '2023-07-12T00:00:00Z',
                                         'Min heap used (MB)': 115.64,
                                         'Max heap used (MB)': 511.06},
                '2023-07-26T00:00:00Z': {'date': '2023-07-26T00:00:00Z',
                                         'Min heap used (MB)': 117.18,
                                         'Max heap used (MB)': 545.65},
                '2023-08-09T00:00:00Z': {'date': '2023-08-09T00:00:00Z',
                                         'Min heap used (MB)': 111.84,
                                         'Max heap used (MB)': 483.33},
                '2023-08-23T00:00:00Z': {'date': '2023-08-23T00:00:00Z',
                                         'Min heap used (MB)': 114.26,
                                         'Max heap used (MB)': 503.5},
                '2023-09-06T00:00:00Z': {'date': '2023-09-06T00:00:00Z',
                                         'Min heap used (MB)': 116.66,
                                         'Max heap used (MB)': 554.82},
                '2023-09-20T00:00:00Z': {'date': '2023-09-20T00:00:00Z',
                                         'Min heap used (MB)': 103.79,
                                         'Max heap used (MB)': 521.74}}

        expected_plots = {
            'Min heap used (MB)': [88.37, 93.24, 93.12, 93.36, 90.34, 90.57, 88.31,
                                   89.99, 85.4, 94.67, 83.31, 108.68, 90.29, 96.5,
                                   94.72, 112.4, 109.7, 115.64, 117.18, 111.84, 114.26,
                                   116.66, 103.79],
            'Max heap used (MB)': [360.79, 357.57, 489.0, 339.98, 448.27, 343.99,
                                   389.67, 334.34, 340.25, 362.89, 406.11, 474.59,
                                   396.23, 448.06, 362.23, 483.55, 478.83, 511.06,
                                   545.65, 483.33, 503.5, 554.82, 521.74]}

        dates, plots = convert_to_plot(test, metrics)
        self.assertEqual(expected_plots, plots)
        self.assertEqual(expected_dates, dates)
