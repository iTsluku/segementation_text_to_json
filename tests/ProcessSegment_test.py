import unittest
from special_court_munich import process_segment


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
            process_segment.get_number_of_people_involved_in_process(process_text)
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
            process_segment.get_first_name_of_people_involved_in_process(process_text)
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
            process_segment.get_last_name_of_people_involved_in_process(process_text)
        )
        self.assertEqual(
            expected_last_name_of_people_involved_in_process, last_name_people_output
        )

    def test_get_last_name_of_people_involved_in_process_look_ahead(self):
        process_text = "... Test NSDAP-Blabla ..."
        wrong_output = ["NSDAP"]
        last_name_person_output = (
            process_segment.get_last_name_of_people_involved_in_process(process_text)
        )
        self.assertNotEqual(wrong_output, last_name_person_output)

    def test_get_multiple_first_name_of_people_involved_in_process(self):
        process_text = (
            "Prozeß gegen den Bäcker Peter Markus PREISSL (geb.28. Jun. 1911) "
            "aus Himmelmoos Gde. Niederaudorf (Lkr. Rosenheim)..."
        )
        expected_output = ["Peter Markus"]
        full_first_name_person_output = (
            process_segment.get_first_name_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_output, full_first_name_person_output)

    def test_prefix_variation_before_occupation(self):
        process_text = (
            "Prozeß gegen die Bäckermeisterin Anna Maria PREISSL (geb.28. Jun. 1911) "
            "aus Himmelmoos Gde. Niederaudorf (Lkr. Rosenheim)..."
        )
        expected_output = ["Bäckermeisterin"]
        full_first_name_person_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
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
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_occupation_prefix_look_behind(self):
        process_text = (
            " den Gastwirt Artur STEGMANN(geb. 21. Okt. 1899), NSDAP-Stützpunktleiter,"
            "den Schuhmacher Jakob HABRES (geb. 3. Jun.1900), Vorstand des"
        )
        expected_output = ["Gastwirt", "Schuhmacher"]
        full_first_name_person_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
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
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_get_multiple_occupation_for_people_involved_in_process(
        self,
    ):
        process_text = "Prozeß gegen den Kunsthistoriker und Heimatforscher Wilhelm KAISER (geb.7. Spt.1890)"
        expected_occupations = ["Kunsthistoriker und Heimatforscher"]
        occupations_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_occupation_prefix_ldw(self):
        process_text = (
            "Prozeß gegen die ldw. Arbeiterin Viktoria WUNDER (geb. 12. Mai 1918) aus Prittriching "
            "(Lkr. Landsberg) wegen verbotenenUmgangs mit dem französischen Kriegsgefangenen George BOLLET."
        )
        expected_occupations = ["ldw. Arbeiterin"]
        occupations_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_occupation_prefix_kath(self):
        process_text = (
            "Prozeß gegen den kath. Pfarrer Franz Xaver DUSCHL (geb. 17. Feb. 1875) aus Mittich(Lkr. Griesbach) "
            "wegen der Behauptung, eswürden nicht alle Kriegsverluste bekanntgegeben, um das Volk nicht zu beunruhigen."
            " Urteil: 3 Monate Gefängnis$ 2 HG; 8 130a StGB)27. Dez. 1940 - 19. Dez. 1941(1 KMs So 59/41)"
        )
        expected_occupations = ["kath. Pfarrer"]
        occupations_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_occupation_prefix_kfm(self):
        process_text = (
            "Prozeß gegen den kfm. Angestellten Franz MAYER (geb. 24. Mrz. 1907) aus Münchenwegen Urkundenfälschung."
            "Urteil: 10 Monate Gefängnis(33 267,268 StGB)3. Jan. 1941 - 30. Jun. 1944(5 KLs So 57/41)"
        )
        expected_occupations = ["kfm. Angestellten"]
        occupations_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_occupation_prefix_landw(self):
        process_text = (
            "Prozeß gegen den landw. Arbeiter Johann ZOTT (geb. 22. Jan. 1921) aus Vohburg(Lkr. Pfaffenhofen) "
            "wegen versuchten Diebstahls.Urteil: 1 Jahr 3 Monate Gefängnis"
            "(88 43,44,242-244 StGB; $ 2 WVO)31. Jan. 1941 - 25. Mai 1942(4 KLs So 18/41)"
        )
        expected_occupations = ["landw. Arbeiter"]
        occupations_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_get_additional_person_data(self):
        process_text = (
            "Ermittlungsverfahren gegen den Landwirt und "
            "Bürgemeister Johann OHMEIER (geb.11. Okt. 1881), BVP-Mitglied aus Buch (Lkr.Illertissen), "
            "den Gastwirt Artur STEGMANN(geb. 21. Okt. 1899), NSDAP-Stützpunktleiter,"
            "den Schuhmacher Jakob HABRES (geb. 3. Jun.1900), Vorstand des kath. Burschenvereins inBuch, "
            "den Schreiner Anton DOPFER (geb. 19. Apr. 1910), NSDAPMitglied und Hilfspolizist, "
            "den Ingenieur Karl BIBER (geb. 4. Dez. 1907) aus Dattenhausen (Lkr. Illertissen) "
            "wegen Bedrohungdes Hauptlehrers Hörmann, der in Verdachtstand, er habe "
            "den Pater Arno SCHOLZEN ausSt. Ottilien in Schutzhaft nehmen lassen,da er eine "
            "Hitlerbüste im Schulhaus vomFlügel an das Fenster gestellt nat.Eröffnung "
            "der Hauptverhandlung abgelehnt23. Jun. 1933 - 30. Okt. 1933(So E 34/33)"
        )
        expected_output = [
            ("Johann", "OHMEIER", "BVP-Mitglied aus Buch (Lkr.Illertissen)"),
            ("Artur", "STEGMANN", "NSDAP-Stützpunktleiter"),
            ("Jakob", "HABRES", "Vorstand des kath. Burschenvereins inBuch"),
            ("Anton", "DOPFER", "NSDAPMitglied und Hilfspolizist"),
            ("Karl", "BIBER", "aus Dattenhausen (Lkr. Illertissen)"),
        ]
        additional_person_data = process_segment.get_additional_person_data(
            process_text
        )
        self.assertEqual(expected_output, additional_person_data)

    def test_get_additional_data_two_people_same_location(self):
        process_text = (
            "Prozeß gegen den Zimmermann Kaspar SEEBERGER (geb. 6. Jan. 1902) und dessenBruder, "
            "den Zimmermeister Xaver SEEBERGER(geb. 7. Okt. 1896), "
            "beide aus Marktoffingen (Lkr. Nördlingen), wegen derBehauptung, "
            'auf einem Auto mit SA-Leutensei gestanden "Hier werden Ablässe verkauft".'
            "Urteil: Kaspar S. Freispruch;Xaver 58. "
            "Verfahren eingestellt6. Spt. 1935 - 17. Jun. 1936(AK 119/36)"
        )
        expected_output = [
            ("Kaspar", "SEEBERGER", "aus Marktoffingen (Lkr. Nördlingen)"),
            ("Xaver", "SEEBERGER", "aus Marktoffingen (Lkr. Nördlingen)"),
        ]
        additional_person_data = process_segment.get_additional_person_data(
            process_text
        )
        self.assertEqual(expected_output, additional_person_data)

    def test_get_additional_data_all_people_same_location(self):
        process_text = (
            "Prozeß gegen den Schuhmacher Josef DAVID(geb. 22. Jan. 1899), den Heizer Heinrich DAVID "
            "(geb. 14. Spt. 1897), den Schneider Johann WEIDINGER (geb. 22, Okt. 1895),alle aus München, "
            "wegen Verbreitungkommunistischer Flugblätter."
        )
        expected_output = [
            ("Josef", "DAVID", "aus München"),
            ("Heinrich", "DAVID", "aus München"),
            ("Johann", "WEIDINGER", "aus München"),
        ]
        additional_person_data = process_segment.get_additional_person_data(
            process_text
        )
        self.assertEqual(expected_output, additional_person_data)

    def test_get_additional_data_remove_and_case(self):
        process_text = (
            "Prozeß gegen den Hilfsarbeiter Hermann FABER (geb. 15. Nov. 1920) "
            "und den Gärtner Hugo SATTLER (geb. 17. Mrz.1921) wegen Gefangenenmeuterei in "
            "Kaufbeuren.Urteil: Faber 6 Jahre Zuchthaus; Sattler5 Jahre Zuchthaus; "
            "Faber und Sattler Aberkennung der bürgerlichenEhrenrechte auf je 3 Jahre."
            "(3 1 Ges.z.Gewährl.d.Rechtsfriedens)27. Mrz. 1940 - 14. Apr. 1944(1 KLs So 133/40)"
        )
        expected_output = []
        bad_output = [("Hermann", "FABER", "und")]
        additional_person_data = process_segment.get_additional_person_data(
            process_text
        )
        self.assertEqual(expected_output, additional_person_data)
        self.assertNotEqual(bad_output, additional_person_data)

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
        birthday_output = process_segment.get_birthday_of_people_involved_in_process(
            process_text
        )
        self.assertEqual(expected_output, birthday_output)

    def test_get_birthday_orc_dot_comma(self):
        process_text = (
            "Prozeß gegen den Schlosser Alois HAXPCINTNER (geb. 10. Jun, 1893)"
        )
        expected_output = ["1893-06-10"]
        birthday_output = process_segment.get_birthday_of_people_involved_in_process(
            process_text
        )
        self.assertEqual(expected_output, birthday_output)

    def test_ignore_nationality_occupation_prefix(self):
        process_text = (
            "Prozeß gegen den polnischen Hilfsarbeiter Jan BAYNO (geb. 8. Dez. 1917) aus "
            "Münchenwegen versuchter Nowtzucht.Urteil: 3 Jahre Zuchthaus, 3 Jahre Ehrverlust"
            "(83 43,177 SB)4. Jun. 7941 - 14. A 1944(4 KLs So 46/41)"
        )
        expected_occupations = ["Hilfsarbeiter"]
        occupations_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_ignore_ethnic_affiliation_occupation_prefix(self):
        process_text = (
            "Prozeß gegen den jüdischen Kaufmann Hermann LEESER (geb. 2. Feb. 1884) aus Bad Ischl,den "
            "Geschäftsführer Otto SZAMEITAT (geb.24. Aug. 1896), die Haushälterin Martha STUSCHE "
            "(geb. 13. Mrz. 1884), die Buchhalterin Auguste SCHOLTEN (geb. 6. Okt. 1892),"
            "die Direktrice Anna VEH (geb. 20. Jun. 1902),die Pensionistensehefrau Anna VEH "
            "(geb.30. Mai 1874), alle aus Augsburg und den Ingenieur Theodor FRIEDRICH aus Bad Aussee,"
            "wegen Devisenvergehens.Verfahren gegen Friedrich wegen Verjährungeingestellt; "
            "Verfahren gegen Anna Veh (altund jung) wegen Amnestie eingestellt; "
            "Verfahren gegen Auguste Scholten eingestellt.Leeser gest. 27. Feb. 1938 in Auslieferungshaft."
            "Urteil: Szameitat 2 Jahre 10 Monate Zuchthaus, Geldstrafe oder 50 Tage Gefängnis, "
            "Aberkennung der bürgerlichen Ehrenrechte auf 4 Jahre;Stusche 1 Jahr 3 Monate "
            "Gefängnis,Geldstrafe oder 21 Tage Gefängnis"
            "(Devisengesetze; VVG)8. Feb. 1938 - 15. Jul. 1941(2 KMs So 2/39)"
        )
        expected_occupations = [
            "Kaufmann",
            "Geschäftsführer",
            "Haushälterin",
            "Buchhalterin",
            "Direktrice",
            "Pensionistensehefrau",
            "Ingenieur",
        ]
        occupations_output = (
            process_segment.get_occupation_of_people_involved_in_process(process_text)
        )
        self.assertEqual(expected_occupations, occupations_output)

    def test_get_proceeding_id(self):
        process_text = (
            "Prozeß gegen den kfm. Angestellten Franz MAYER (geb. 24. Mrz. 1907) aus Münchenwegen Urkundenfälschung."
            "Urteil: 10 Monate Gefängnis(33 267,268 StGB)3. Jan. 1941 - 30. Jun. 1944(5 KLs So 57/41)"
        )
        expected_verdict_paragraph = "(5 KLs So 57/41)"
        try:
            verdict_paragraph_output = process_segment.get_registration_no(process_text)
            self.assertEqual(expected_verdict_paragraph, verdict_paragraph_output)
        except process_segment.ProcessCaseIdException as e:
            self.fail(e.message)

    def test_get_id_of_last_proceeding_given_a_page(self):
        process_text = (
            "Prozeß gegen den Taglöhner Josef VIELHUBER (geb. 5. Dez. 1871) aus Oberhaching bei "
            "München wegen Anschlagens dreier handschriftlicher Zettel gegen den NS. Urteil: 8 Monate Gefängnis "
            "Anlage: Die inkriminierten Zettel 6. Jul. 1933 - 7. Mrz. 1935 | (S Pr 225/33) 38 "
        )
        expected_verdict_paragraph = "(S Pr 225/33)"
        try:
            verdict_paragraph_output = process_segment.get_registration_no(process_text)
            self.assertEqual(expected_verdict_paragraph, verdict_paragraph_output)
        except process_segment.ProcessCaseIdException as e:
            self.fail(e.message)

    def test_get_id_not_birthday(self):
        process_text = (
            "Prozeß gegen den Hilfsarbeiter Bruno WESTERMEIER (geb. 15. Jun. 1900) ausMünchen, "
            "die Hilfsarbeitersehefrau Ottilie GRIMM (geb. 10. Jul. 1891) unddie Hausangestellte Ottilie "
            "Karolina |WENSAUER (geb. 14. Nov. 1914), beide ausMünchen, wegen Verbreitung "
            "kommunistischerFlugschriften.Urteil: Westermeier 5 Monate Gefängnis,Grimm und Wensauer Freispruch22."
            "Au 1935 - 10. Feb. 1934rs Pr 5161337"
        )
        # wrong_output = "geb. 14. Nov. 1914"
        self.assertRaises(
            process_segment.ProcessCaseIdException,
            process_segment.get_registration_no,
            process_text,
        )

    def test_get_accusations(self):
        process_text = (
            "Prozeß gegen den Dienstknecht Johann WILLE (geb. 31. Mai 1909) und "
            "die Metzgerswitwe Katharina BRAUN (geb. 10. Mai 1892), beide aus Neuburg a.d. Donau, "
            "wegen Diebstahls. Urteils Wille 2 Jahre 6 Monate Zuchthaus, 5 Jahre Ehrverlust; "
            "Braun Frei spruch (8 1 KWVO; 88 242, 243 STGB; ° 2 VVO) 20, Jul. 1944 28. Mrz. 1945 (3 SKLs 488/44)"
        )
        expected_output = [("WILLE", "Diebstahls"), ("BRAUN", "Diebstahls")]
        accusation_output = process_segment.get_accusations(process_text)
        self.assertEqual(expected_output, accusation_output)

    def test_get_accusations_no_urteil(self):
        process_text = (
            "Ermittlungsverfahren gegen den Hausierer Andreas MANGERTSEDER (sed. 27, Nov. 1864 , gest. 13. Mai 1936) "
            "aus Pfarrkirchen wegen einer kritischen Außerun über Hitler. "
            "Verfahren wegen Todes des Angeklagten eingestellt 26, Mrz. 1936 24, Nov. 1936 (16 KMs So 169/36)"
        )
        expected_output = [("MANGERTSEDER", "einer kritischen Außerun über Hitler")]
        accusation_output = process_segment.get_accusations(process_text)
        self.assertEqual(expected_output, accusation_output)

    def test_get_result_prozess(self):
        process_text = (
            "Prozeß gegen den Vertreter Martin GRAF (geb. 1. Mai 1895) aus Traunstein wesen Betrugs. "
            "Urteil: 2 Jahre Gefängnis (88 263,267,268 StGB) 2, Jun, 1942 13. Apr. 1944 (4 KLs So 134/42)"
        )
        expected_output = [
            (
                "GRAF",
                "Urteil: 2 Jahre Gefängnis",
            )
        ]
        result_output = process_segment.get_result(process_text)
        self.assertEqual(expected_output, result_output)

    def test_get_result_prozess_no_law(self):
        process_text = (
            "Prozeß gegen den Former Johann Wilhelm KRAMER (zed. 9. Mai 1909) aus München wegen der Behauptung, "
            'es seien schon mehr als "00 Kommunisten erschossen worden. Vorführung aus der Schutzhaft. '
            "Urteil: 5 Monate Haft 3. Apr. 1933 19. Spt. 1934 (S Pr 8/33)"
        )
        expected_output = [
            (
                "KRAMER",
                "Urteil: 5 Monate Haft",
            )
        ]
        result_output = process_segment.get_result(process_text)
        self.assertEqual(expected_output, result_output)

    def test_get_result_prozess_anklage_zurückgenommen(self):
        process_text = (
            "Prozeß gegen die Geschäftsinhaberin Maria LANG (geb. 28. Spt. 1886) und den Kaufmann und Geschäftsinhaber "
            "Josef HAUSNER (geb. 8. Spt. 1890), beide aus München, wegen Zurückhaltens von Textilwaren. “ “ (% 1 KWVO) "
            "Anklage zurückgenommen 12. Mrz. 1942 3. Spt. 1944 (2 KLs So 205/42) a \\ 2 , e . * j ar un"
        )
        expected_output = [
            (
                "LANG",
                "Anklage zurückgenommen",
            ),
            ("HAUSNER", "Anklage zurückgenommen"),
        ]
        result_output = process_segment.get_result(process_text)
        self.assertEqual(expected_output, result_output)

    def test_get_result_ermittlungsverfahren(self):
        process_text = (
            " Ermittlungsverfahren gegen den Möbelschreiner Paul SOLLANECK (geb, 4. Okt. 1896) "
            "aus München, weil er abfällige Bemerkungen über die Usterreicher machte, "
            "Verfahren eingestellt 7. Nov. 1938 5. Dez. 1938 (1d Js So 2172/38)"
        )
        expected_output = [("SOLLANECK", "Verfahren eingestellt")]
        result_output = process_segment.get_result(process_text)
        self.assertEqual(expected_output, result_output)

    def test_get_result_filter_anlagen(self):
        process_text = (
            "Prozeß gegen die Hilfsarbeitersehefrau Maria SCHRAUFSTETTER (geb, 27. Aug. 1886) "
            "aus München wegen unerlaubten Verteilens von kommunistischen Flugblättern., "
            "Urteil: Freispruch nach Untersuchungshaft Anlage: 2 hektographierte Flugblätter "
            'der "Rot Front" 21. Mrz. 1933 16, Mai 1933 (S Pr 2/33)'
        )
        expected_output = [
            ("SCHRAUFSTETTER", "Urteil: Freispruch nach Untersuchungshaft")
        ]
        result_output = process_segment.get_result(process_text)
        self.assertEqual(expected_output, result_output)

    def test_get_duration(self):
        process_text = (
            " Ermittlungsverfahren gegen den Möbelschreiner Paul SOLLANECK (geb, 4. Okt. 1896) "
            "aus München, weil er abfällige Bemerkungen über die Usterreicher machte, "
            "Verfahren eingestellt 7. Nov. 1938 5. Dez. 1938 (1d Js So 2172/38)"
        )
        expected_output = "7. Nov. 1938 5. Dez. 1938"
        duration = process_segment.get_duration(process_text)
        self.assertEqual(expected_output, duration)

    def test_get_duration_split(self):
        process_text = (
            " Ermittlungsverfahren gegen den Möbelschreiner Paul SOLLANECK (geb, 4. Okt. 1896) "
            "aus München, weil er abfällige Bemerkungen über die Usterreicher machte, "
            "Verfahren eingestellt 7. Nov. 1938 - 5. Dez. 1938 (1d Js So 2172/38)"
        )
        expected_output = "7. Nov. 1938 - 5. Dez. 1938"
        duration = process_segment.get_duration(process_text)
        self.assertEqual(expected_output, duration)

    def test_get_duration_ocr_fail(self):
        process_text = (
            "Prozeß gegen die Hilfsarbeitersehefrau Maria SCHRAUFSTETTER (geb, 27. Aug. 1886) "
            "aus München wegen unerlaubten Verteilens von kommunistischen Flugblättern., "
            "Urteil: Freispruch nach Untersuchungshaft Anlage: 2 hektographierte Flugblätter der "
            '"Rot Front" 21. Mrz. 1933 16, Mai 1933 (S Pr 2/33)'
        )
        expected_output = "21. Mrz. 1933 16, Mai 1933"
        duration = process_segment.get_duration(process_text)
        self.assertEqual(expected_output, duration)

    def test_get_law(self):
        process_text = (
            "Prozeß gegen den Vertreter Martin GRAF (geb. 1. Mai 1895) aus Traunstein wesen Betrugs. "
            "Urteil: 2 Jahre Gefängnis (88 263,267,268 StGB) 2, Jun, 1942 13. Apr. 1944 (4 KLs So 134/42)"
        )
        expected_output = [
            (
                "GRAF",
                "(88 263,267,268 StGB)",
            )
        ]
        law_output = process_segment.get_law(process_text)
        self.assertEqual(expected_output, law_output)

    def test_get_attachments(self):
        process_text = (
            "Prozeß gegen die Hilfsarbeitersehefrau Maria SCHRAUFSTETTER (geb, 27. Aug. 1886) "
            "aus München wegen unerlaubten Verteilens von kommunistischen Flugblättern., "
            "Urteil: Freispruch nach Untersuchungshaft Anlage: 2 hektographierte Flugblätter der "
            '"Rot Front" 21. Mrz. 1933 16, Mai 1933 (S Pr 2/33)'
        )
        expected_output = [
            ("SCHRAUFSTETTER", 'Anlage: 2 hektographierte Flugblätter der "Rot Front"')
        ]
        attachements = process_segment.get_attachments(process_text)
        self.assertEqual(expected_output, attachements)
