import unittest
from ocr import PreprocessOcrOutput


class TestPreprocessOcrOutput(unittest.TestCase):
    def test_fix_first_last_name_no_whitespace(self):
        ocr_output = (
            "Prozeß gegen die Monteurin KatharinaGRAS-BERGER (geb. 29. Dez. 1910) und den kfm. "
            "Angestellten FritzWÜNSCHE (geb. 10. Jan. 1906) aus München wegen Verbreitung "
            "kommu-nistischer Druckschriften. "
        )
        expected_result = (
            "Prozeß gegen die Monteurin Katharina GRAS-BERGER (geb. 29. Dez. 1910) und den kfm. "
            "Angestellten Fritz WÜNSCHE (geb. 10. Jan. 1906) aus München wegen Verbreitung "
            "kommu-nistischer Druckschriften. "
        )
        preprocessed_ocr_output = PreprocessOcrOutput.fix_first_last_name_no_whitespace(
            ocr_output
        )
        self.assertEqual(expected_result, preprocessed_ocr_output)
