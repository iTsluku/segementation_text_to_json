import unittest
from ocr import ParseProcessSegements


class TestParseProcessSegments(unittest.TestCase):
    def test_get_number_of_people_involved_in_process(self):
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
        expected_number_of_people_involved_in_process = 8  # not 11!
        number_of_people_output = (
            ParseProcessSegements.get_number_of_people_involved_in_process(process_text)
        )
        self.assertEqual(
            expected_number_of_people_involved_in_process, number_of_people_output
        )

    def test_get_first_name_of_people_involved_in_process(self):
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
        expected_first_name_of_people_involved_in_process = [
            "Alois",
            "Johann",
            "Fritz",
            "Ludwig",
            "Gottfried",
            "Josef",
            "Anton",
            "Josef",
        ]
        first_name_people_output = (
            ParseProcessSegements.get_first_name_of_people_involved_in_process(
                process_text
            )
        )
        self.assertEqual(
            expected_first_name_of_people_involved_in_process,
            first_name_people_output,
        )

    def test_get_last_name_of_people_involved_in_process(self):
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
        expected_last_name_of_people_involved_in_process = [
            "DUNST",
            "BRAUNWIESER",
            "EGGER",
            "BACHMANN",
            "REISCHL",
            "HUBER",
            "HUBER",
            "TRIENDL",
        ]
        last_name_people_output = (
            ParseProcessSegements.get_last_name_of_people_involved_in_process(
                process_text
            )
        )
        self.assertEqual(
            expected_last_name_of_people_involved_in_process, last_name_people_output
        )

    def test_get_last_name_of_people_involved_in_process_look_ahead(self):
        process_text = "... Test NSDAP-Blabla ..."
        wrong_output = ["NSDAP"]
        last_name_person_output = (
            ParseProcessSegements.get_last_name_of_people_involved_in_process(
                process_text
            )
        )
        self.assertNotEqual(wrong_output, last_name_person_output)

    def test_get_multiple_first_name_of_people_involved_in_process(self):
        process_text = (
            "Prozeß gegen den Bäcker Peter Markus PREISSL (geb.28. Jun. 1911) "
            "aus Himmelmoos Gde. Niederaudorf (Lkr. Rosenheim)..."
        )
        expected_output = ["Peter Markus"]
        full_first_name_person_output = (
            ParseProcessSegements.get_first_name_of_people_involved_in_process(
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
            ParseProcessSegements.get_occupation_of_people_involved_in_process(
                process_text
            )
        )
        self.assertEqual(expected_output, full_first_name_person_output)

    def test_get_occupation_of_people_involved_in_process(self):
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
        expected_occupations = [
            "Bauhilfsarbeiter",
            "Maurer",
            "Dachdecker",
            "Friseur",
            "Mechaniker",
            "Maler",
            "Mau-rer",
            "Maler",
        ]
        occupations_output = (
            ParseProcessSegements.get_occupation_of_people_involved_in_process(
                process_text
            )
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_occupation_prefix_look_behind(self):
        process_text = (
            " den Gastwirt Artur STEGMANN(geb. 21. Okt. 1899), NSDAP-Stützpunktleiter,"
            "den Schuhmacher Jakob HABRES (geb. 3. Jun.1900), Vorstand des"
        )
        expected_output = ["Gastwirt", "Schuhmacher"]
        full_first_name_person_output = (
            ParseProcessSegements.get_occupation_of_people_involved_in_process(
                process_text
            )
        )
        self.assertEqual(expected_output, full_first_name_person_output)

    def test_get_occupation_multiple_capital_in_first_name_of_people_involved_in_process(
        self,
    ):
        process_text = (
            "Prozeß gegen die Küchengehilfin MariaAnna HEINZMANN (geb. 6. Jul. 1893) ausAugsburg "
            "wegen abwertender Bemerkungenüber Hitler.Urteil: 8 Monate Gefängnis&$ 2 HG)"
            "4. Jul. 1941 - 14. Spt. 1942(1 KMs So 197/41)"
        )
        expected_occupations = ["Küchengehilfin"]
        occupations_output = (
            ParseProcessSegements.get_occupation_of_people_involved_in_process(
                process_text
            )
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_get_multiple_occupation_for_people_involved_in_process(
        self,
    ):
        process_text = "Prozeß gegen den Kunsthistoriker und Heimatforscher Wilhelm KAISER (geb.7. Spt.1890)"
        expected_occupations = ["Kunsthistoriker, Heimatforscher"]
        occupations_output = (
            ParseProcessSegements.get_occupation_of_people_involved_in_process(
                process_text
            )
        )
        # TODO
        # self.assertEqual(expected_occupations, occupations_output)

    def test_additional_info(self):
        # TODO add additional info to person :: e.g. BVP-Mitglied aus Buch (Lkr.Illertissen) for Johann OHMEIER
        process_text = (
            "Ermittlungsverfahren gegen den Landwirt undehemaligen "
            "Bürgemeister Johann OHMEIER (geb.11. Okt. 1881), BVP-Mitglied aus Buch (Lkr.Illertissen), "
            "den Gastwirt Artur STEGMANN(geb. 21. Okt. 1899), NSDAP-Stützpunktleiter,"
            "den Schuhmacher Jakob HABRES (geb. 3. Jun.1900), Vorstand des kath. Burschenvereins inBuch, "
            "den Schuhmacher Xaver DOPFER (get. 6.1907), NSDAP-Mitglied, Hilfspolizist ausUnterroth (Lkr. Illertissen), "
            "den Schreiner Anton DOPFER (geb. 19. Apr. 1910), NSDAPMitglied und Hilfspolizist, "
            "den Ingenieur Karl BIBER (geb. 4. Dez. 1907) aus Dattenhausen (Lkr. Illertissen) "
            "wegen Bedrohungdes Hauptlehrers Hörmann, der in Verdachtstand, er habe "
            "den Pater Arno SCHOLZEN ausSt. Ottilien in Schutzhaft nehmen lassen,da er eine "
            "Hitlerbüste im Schulhaus vomFlügel an das Fenster gestellt nat.Eröffnung "
            "der Hauptverhandlung abgelehnt23. Jun. 1933 - 30. Okt. 1933(So E 34/33)"
        )

    def test_get_birthday_of_people_involved_in_process(self):
        process_text = (
            "Ermittlungsverfahren gegen den Landwirt undehemaligen "
            "Bürgemeister Johann OHMEIER (geb. 11. Okt. 1881), BVP-Mitglied aus Buch (Lkr.Illertissen), "
            "den Gastwirt Artur STEGMANN(geb. 21. Okt. 1899), NSDAP-Stützpunktleiter,"
            "den Schuhmacher Jakob HABRES (geb. 3. Jun.1900), Vorstand des kath. Burschenvereins inBuch, "
            "den Schreiner Anton DOPFER (geb. 19. Apr. 1910), NSDAPMitglied und Hilfspolizist, "
            "den Ingenieur Karl Dietrich BIBER (geb. 4. Dez. 1907) aus Dattenhausen (Lkr. Illertissen) "
        )
        expected_output = [
            "1881-10-11",
            "1899-10-21",
            "1900-06-03",
            "1910-04-19",
            "1907-12-04",
        ]
        birthday_output = (
            ParseProcessSegements.get_birthday_of_people_involved_in_process(
                process_text
            )
        )
        self.assertEqual(expected_output, birthday_output)
