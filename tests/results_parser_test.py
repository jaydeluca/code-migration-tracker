import unittest

from results_parser import parse


class ResultsParserTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.example = """----------------------------------------------------------\n Run at Sat Sep 23 05:22:19 UTC 2023\n release : compares no agent, latest stable, and latest snapshot agents\n 5 users, 5000 iterations\n----------------------------------------------------------\nAgent               :              none           latest         snapshot\nRun duration        :          00:02:27         00:02:57         00:03:06\nAvg. CPU (user) %   :        0.46024063       0.48809186       0.49900937\nMax. CPU (user) %   :         0.5527638        0.5891089              0.6\nAvg. mch tot cpu %  :         0.9943353       0.99306744        0.9932704\nStartup time (ms)   :             19598            16351            17050\nTotal allocated MB  :          27799.50         34195.20         58039.97\nMin heap used (MB)  :             88.10           115.85           112.63\nMax heap used (MB)  :            365.90           557.00           478.78\nThread switch rate  :          28534.94        29848.291        32354.986\nGC time (ms)        :              1800             3014             2928\nGC pause time (ms)  :              1814             3052             2959\nReq. mean (ms)      :             10.74            12.82            13.51\nReq. p95 (ms)       :             32.04            38.45            40.28\nIter. mean (ms)     :            144.60           173.90           182.65\nIter. p95 (ms)      :            233.74           275.94           291.89\nNet read avg (bps)  :        5441971.00       4728712.00       4507975.00\nNet write avg (bps) :        7256048.00      25533599.00      24434992.00\nPeak threads        :                43               55               56\n"""
        self.metrics = [
            "Min heap used (MB)",
            "Max heap used (MB)"
        ]
        super(ResultsParserTestCase, self).__init__(*args, **kwargs)

    def test_parse_metrics_from_summary(self):
        result = parse(report=self.example, metrics=self.metrics)
        self.assertEqual(557.00, result.metrics["Max heap used (MB)"])
        self.assertEqual(115.85, result.metrics["Min heap used (MB)"])

    def test_parse_date_from_summary(self):
        result = parse(report=self.example, metrics=self.metrics)
        self.assertEqual("2023-09-23", result.date)


