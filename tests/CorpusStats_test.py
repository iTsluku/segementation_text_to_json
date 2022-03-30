import unittest

from special_court_munich.corpus import CorpusStats


class TestCorpusStats(unittest.TestCase):
    def test_inc_val(self):
        input_values = [-5, -1, 0, 9]
        expected_output_values = [-4, 0, 1, 10]
        output_values = [CorpusStats.inc_val(x) for x in input_values]
        for i, v in enumerate(output_values):
            self.assertEqual(expected_output_values[i], v)
            self.assertTrue(v > input_values[i])
            self.assertEqual(input_values[i], v - 1)
