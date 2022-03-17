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

    def test_add_missing_whitespace_before_occupation(self):
        ocr_output = (
            "Prozeß gegen dieBeruf und Polsterer Anna FRÖMBECK (geb. 3. Jun 10919), "
            "denMaurer Ferdinand FROHLICH (geb. 29. Aug.1920), den Schlosser Rudolf KIENLE (geb.8. Spt. 1922), "
            "den Hilfsarbeiter Ludwig BADER (geb. 11. Nov. 1921), alle aus München, "
            "wegen versuchten Diebstahls. .Urteil: Fröhlich unter Einrechnung derStrafe des "
            "So G-M vom 20. Mai1940 3 Jahre Zuchthaus; Kienle5 Monate Gefängnis; Frombeck unterEinrechnung "
            "der Strafe des SoG-Mvom 8. Mai 1940 2 Jahre Gefängnis;"
            "Bader Freispruch(885 5,6,9 JGG; 88 43,242-245 StGB)29. Nov. 1940 - 16. Jun. 1944(4 KLs So 14/41)"
        )
        expected_result = (
            "Prozeß gegen die Beruf und Polsterer Anna FRÖMBECK (geb. 3. Jun 10919), "
            "den Maurer Ferdinand FROHLICH (geb. 29. Aug.1920), den Schlosser Rudolf KIENLE (geb.8. Spt. 1922), "
            "den Hilfsarbeiter Ludwig BADER (geb. 11. Nov. 1921), alle aus München, "
            "wegen versuchten Diebstahls. .Urteil: Fröhlich unter Einrechnung derStrafe des "
            "So G-M vom 20. Mai1940 3 Jahre Zuchthaus; Kienle5 Monate Gefängnis; Frombeck unterEinrechnung "
            "der Strafe des SoG-Mvom 8. Mai 1940 2 Jahre Gefängnis;"
            "Bader Freispruch(885 5,6,9 JGG; 88 43,242-245 StGB)29. Nov. 1940 - 16. Jun. 1944(4 KLs So 14/41)"
        )
        preprocessed_ocr_output = (
            PreprocessOcrOutput.add_missing_whitespace_before_occupation(ocr_output)
        )
        self.assertEqual(expected_result, preprocessed_ocr_output)

    def test_add_missing_whitespace_before_word_und(self):
        ocr_output = "den Metzgerund Gastwirt Xaver SCHMATZ (geb. 17. Feb.1867)"
        expected_result = "den Metzger und Gastwirt Xaver SCHMATZ (geb. 17. Feb.1867)"
        preprocessed_ocr_output = (
            PreprocessOcrOutput.add_missing_whitespace_before_and_after_word_und(
                ocr_output
            )
        )
        self.assertEqual(expected_result, preprocessed_ocr_output)

    def test_add_missing_whitespace_after_word_und(self):
        ocr_output = "den Metzger undGastwirt Xaver SCHMATZ (geb. 17. Feb.1867)"
        expected_result = "den Metzger und Gastwirt Xaver SCHMATZ (geb. 17. Feb.1867)"
        preprocessed_ocr_output = (
            PreprocessOcrOutput.add_missing_whitespace_before_and_after_word_und(
                ocr_output
            )
        )
        self.assertEqual(expected_result, preprocessed_ocr_output)

    def test_add_missing_whitespace_before_and_after_word_und(self):
        ocr_output = "den MetzgerundGastwirt Xaver SCHMATZ (geb. 17. Feb.1867)"
        expected_result = "den Metzger und Gastwirt Xaver SCHMATZ (geb. 17. Feb.1867)"
        preprocessed_ocr_output = (
            PreprocessOcrOutput.add_missing_whitespace_before_and_after_word_und(
                ocr_output
            )
        )
        self.assertEqual(expected_result, preprocessed_ocr_output)

    def test_whitespace_occupation_word_und(self):
        ocr_output = (
            "den MetzgerundGastwirt Xaver SCHMATZ (geb. 17. Feb.1867) BlablaundBlabla"
        )
        expected_result = (
            "den Metzger und Gastwirt Xaver SCHMATZ (geb. 17. Feb.1867) BlablaundBlabla"
        )
        wrong_result = "den Metzger und Gastwirt Xaver SCHMATZ (geb. 17. Feb.1867) Blabla und Blabla"
        preprocessed_ocr_output = (
            PreprocessOcrOutput.add_missing_whitespace_before_and_after_word_und(
                ocr_output
            )
        )
        self.assertEqual(expected_result, preprocessed_ocr_output)
        self.assertNotEqual(wrong_result, preprocessed_ocr_output)
