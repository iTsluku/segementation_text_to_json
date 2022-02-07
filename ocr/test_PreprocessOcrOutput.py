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

    def test_split_words_with_multiple_capital_characters_before_occupation(self):
        ocr_output = (
            "Prozeß gegen den VersicherungsinspektorGeorg SCHREYEGG (geo. 10. Apr. 1889) ausMünchen, "
            "früher SPD-Mitglied, wegen Außerungen uber Hitier.Urteil: 2 Jahre 4 Monate Gefängnis"
            "($ 2 HG)6. Okt. 1940 - 19. Feb. 1943(1 KMs So 11/41)"
        )
        expected_result = (
            "Prozeß gegen den Versicherungsinspektor Georg SCHREYEGG (geo. 10. Apr. 1889) ausMünchen, "
            "früher SPD-Mitglied, wegen Außerungen uber Hitier.Urteil: 2 Jahre 4 Monate Gefängnis"
            "($ 2 HG)6. Okt. 1940 - 19. Feb. 1943(1 KMs So 11/41)"
        )
        preprocessed_ocr_output = PreprocessOcrOutput.split_words_with_multiple_capital_characters_before_occupation(
            ocr_output
        )
        self.assertEqual(expected_result, preprocessed_ocr_output)
