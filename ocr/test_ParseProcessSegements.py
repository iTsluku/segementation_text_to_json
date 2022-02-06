import unittest
from ocr import ParseProcessSegements


class TestParseProcessSegments(unittest.TestCase):
    def test_get_number_of_persons_involved_in_process(self):
        process_text = (
            "Prozeß gegen "
            "den Bauhilfsarbeiter Alois DUNST (geb. 11. Jun. 1901), "
            "den Maurer Johann BRAUNWIESER (geb. 11. Nov. 1911), "
            "den Dachdecker Fritz EGGER (geb. 30. Dez. 1912), "
            "den Friseur Ludwig BACHMANN (geb. 16. Aug. 1914), "
            "den Mechaniker Gottfried REISCHL (geb. 17. Okt. 1902), "
            "den Maler Josef HUBER (geb. 7. Mrz. 1913), "
            "den Mau-rer Anton HUBER (geb. 26. Apr. 1914), "
            "den Maler Josef TRIENDL (geb. 18. Okt. 1910), "
            "alle aus Bad Reichenhall, "
            "wegen einer Schlägerei mit Nat.Soz.., "
            "Vorführung aus der Untersuchungshaft. "
            "Urteil: Dunst zwei Jahre und 3 Monate Zuchthaus; "
            "Egger 6 Monate und 1 Woche Gefängnis; "
            "Bachmann 1 Monat Gefängnis; "
            "Reischl 1 Jahr 3 Monate Gefängnis; "
            "Josef und Anton Huber und Triendl je 6 Monate Gefängnis; "
            "Ebenbichler, Hochlechner und Gruber Frei-spruch."
            "1. Feb.1933 - 10. Mai 1935 (S Pr 28 / 33)"
        )
        expected_number_of_persons_involved_in_process = 8  # not 11!
        number_of_persons_output = (
            ParseProcessSegements.get_number_of_persons_involved_in_process(
                process_text
            )
        )
        self.assertEqual(
            expected_number_of_persons_involved_in_process, number_of_persons_output
        )

    def test_get_first_name_of_persons_involved_in_process(self):
        process_text = (
            "Prozeß gegen "
            "den Bauhilfsarbeiter Alois DUNST (geb. 11. Jun. 1901), "
            "den Maurer Johann BRAUNWIESER (geb. 11. Nov. 1911), "
            "den Dachdecker Fritz EGGER (geb. 30. Dez. 1912), "
            "den Friseur Ludwig BACHMANN (geb. 16. Aug. 1914), "
            "den Mechaniker Gottfried REISCHL (geb. 17. Okt. 1902), "
            "den Maler Josef HUBER (geb. 7. Mrz. 1913), "
            "den Mau-rer Anton HUBER (geb. 26. Apr. 1914), "
            "den Maler Josef TRIENDL (geb. 18. Okt. 1910), "
            "alle aus Bad Reichenhall, "
            "wegen einer Schlägerei mit Nat.Soz.., "
            "Vorführung aus der Untersuchungshaft. "
            "Urteil: Dunst zwei Jahre und 3 Monate Zuchthaus; "
            "Egger 6 Monate und 1 Woche Gefängnis; "
            "Bachmann 1 Monat Gefängnis; "
            "Reischl 1 Jahr 3 Monate Gefängnis; "
            "Josef und Anton Huber und Triendl je 6 Monate Gefängnis; "
            "Ebenbichler, Hochlechner und Gruber Frei-spruch."
            "1. Feb.1933 - 10. Mai 1935 (S Pr 28 / 33)"
        )
        expected_first_name_of_persons_involved_in_process = [
            "Alois",
            "Johann",
            "Fritz",
            "Ludwig",
            "Gottfried",
            "Josef",
            "Anton",
            "Josef",
        ]
        first_name_persons_output = (
            ParseProcessSegements.get_first_name_of_persons_involved_in_process(
                process_text
            )
        )
        self.assertEqual(
            expected_first_name_of_persons_involved_in_process,
            first_name_persons_output,
        )

    def test_get_last_name_of_persons_involved_in_process(self):
        process_text = (
            "Prozeß gegen "
            "den Bauhilfsarbeiter Alois DUNST (geb. 11. Jun. 1901), "
            "den Maurer Johann BRAUNWIESER (geb. 11. Nov. 1911), "
            "den Dachdecker Fritz EGGER (geb. 30. Dez. 1912), "
            "den Friseur Ludwig BACHMANN (geb. 16. Aug. 1914), "
            "den Mechaniker Gottfried REISCHL (geb. 17. Okt. 1902), "
            "den Maler Josef HUBER (geb. 7. Mrz. 1913), "
            "den Mau-rer Anton HUBER (geb. 26. Apr. 1914), "
            "den Maler Josef TRIENDL (geb. 18. Okt. 1910), "
            "alle aus Bad Reichenhall, "
            "wegen einer Schlägerei mit Nat.Soz.., "
            "Vorführung aus der Untersuchungshaft. "
            "Urteil: Dunst zwei Jahre und 3 Monate Zuchthaus; "
            "Egger 6 Monate und 1 Woche Gefängnis; "
            "Bachmann 1 Monat Gefängnis; "
            "Reischl 1 Jahr 3 Monate Gefängnis; "
            "Josef und Anton Huber und Triendl je 6 Monate Gefängnis; "
            "Ebenbichler, Hochlechner und Gruber Frei-spruch."
            "1. Feb.1933 - 10. Mai 1935 (S Pr 28 / 33)"
        )
        expected_last_name_of_persons_involved_in_process = [
            "DUNST",
            "BRAUNWIESER",
            "EGGER",
            "BACHMANN",
            "REISCHL",
            "HUBER",
            "HUBER",
            "TRIENDL",
        ]
        last_name_persons_output = (
            ParseProcessSegements.get_last_name_of_persons_involved_in_process(
                process_text
            )
        )
        self.assertEqual(
            expected_last_name_of_persons_involved_in_process, last_name_persons_output
        )

    def test_get_last_name_of_persons_involved_in_process_look_ahead(self):
        process_text = "... Test NSDAP-Blabla ..."
        wrong_output = ["NSDAP"]
        last_name_person_output = (
            ParseProcessSegements.get_last_name_of_persons_involved_in_process(
                process_text
            )
        )
        self.assertNotEqual(wrong_output, last_name_person_output)

    def test_get_multiple_first_name_of_persons_involved_in_process(self):
        process_text = (
            "Prozeß gegen den Bäcker Peter Markus PREISSL (geb.28. Jun. 1911) "
            "aus Himmelmoos Gde. Niederaudorf (Lkr. Rosenheim)..."
        )
        expected_output = ["Peter Markus"]
        full_first_name_person_output = (
            ParseProcessSegements.get_first_name_of_persons_involved_in_process(
                process_text
            )
        )
        self.assertEqual(expected_output, full_first_name_person_output)

    def test_prefix_variation_before_occupation(self):
        process_text = (
            "Prozeß gegen die Bäckermeisterin Anna Maria PREISSL (geb.28. Jun. 1911) "
            "aus Himmelmoos Gde. Niederaudorf (Lkr. Rosenheim)..."
        )
        expected_output = ["Bäckermeisterin"]
        full_first_name_person_output = (
            ParseProcessSegements.get_occupation_of_persons_involved_in_process(
                process_text
            )
        )
        self.assertEqual(expected_output, full_first_name_person_output)
