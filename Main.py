import os
import json
import shutil

from ocr.ParseProcessSegements import (
    get_number_of_people_involved_in_process,
    get_first_name_of_people_involved_in_process,
    get_last_name_of_people_involved_in_process,
    get_occupation_of_people_involved_in_process,
    get_birthday_of_people_involved_in_process,
    get_additional_person_data,
    get_process_case_id,
    ProcessCaseIdException,
)
from ocr.PreprocessOcrOutput import (
    fix_first_last_name_no_whitespace,
    split_words_with_multiple_capital_characters_before_occupation,
    add_missing_whitespace_before_occupation,
    add_missing_whitespace_before_and_after_word_und,
)
from pathlib import Path
from typing import List

cwd = os.getcwd()

parsed_documents_n = 0
parsed_process_segements_n = 0
parsed_process_n = 0
invalid_document_name_n = 0
invalid_id_paragraph_n = 0
invalid_paragraph_segmentation_n = 0
valid_document_n = 0
valid_process_n = 0
no_additional_data_person_n = 0
processed_people = 0
missing_process_case_id_n = 0
invalid_process_checksum = 0


class Error(Exception):
    """Base class for other exceptions."""

    pass


class InvalidDocumentName(Error):
    """Raised when the document name is not valid."""

    pass


class InvalidIdParagraph(Error):
    """Raised when the document id paragraph is not valid."""

    pass


class ParagraphSegmentationException(Error):
    """Raised when the paragraphs can't be segmented."""

    pass


class ExtractProcessDataException(Error):
    """Raised when number of first names, last names or occupations don't add up"""

    pass


def get_old_ids(file_path: str) -> List[str]:
    old_ids = []

    with open(file_path) as f:
        for line in f:
            if line not in ["\n", "\r\n", ""]:
                line = line.strip().replace(".", "")
                if line[0] == "(" and line[-1] == ")":
                    line = line.replace("(", "").replace(")", "")
                    if line.isdigit() and len(line) >= 3:
                        old_ids.append(line)
                else:
                    break
    return old_ids


def get_new_ids(file_path: str) -> List[str]:
    new_ids = []

    with open(file_path) as f:
        for line in f:
            if line not in ["\n", "\r\n", ""]:
                line = line.strip().replace(".", "")
                if line[0] == "(" and line[-1] == ")":
                    continue
                elif line.isdigit() and len(line) >= 4:
                    new_ids.append(line)
                else:
                    break
    return new_ids


def remove_linebreak_hyphen(s: str) -> str:
    o = ""
    prev = ""

    for c in s:
        if c == "\n" and prev == "-":
            prev = ""
        elif c == "\n":
            o += prev
            prev = ""
        else:
            o += prev
            prev = c
    o += prev
    return o


def parse_process_paragraphs(file_path: str, old_ids_n: int) -> List[str]:
    """
    Return empty list if document is invalid.
    """
    process_paragraphs = []
    passed_ids = False
    passed_potential_overlap = False
    p = ""
    temp = ""

    with open(file_path) as f:
        for line in f:
            if not passed_ids:
                if line[0] == "(" or line[0].isdigit() or line in ["\n", "\r\n"]:
                    continue
                else:
                    passed_ids = True
            # passed_ids
            if line in ["\n", "\r\n"]:
                temp = p
                p = ""
            else:
                new_paragraph = False
                if len(line.split()) >= 2:
                    check = line.split()[:2]
                    if (
                        check[0].replace(".", "")
                        in ["Prozeß", "Frozeß", "Ermittlungsverfahren"]
                        and check[1].replace(".", "") == "gegen"
                    ):
                        new_paragraph = True
                        passed_potential_overlap = True
                if new_paragraph and not temp == "":
                    if passed_potential_overlap:
                        process_paragraphs.append(temp)
                        temp = ""
                        p = line
                else:
                    p += temp + line
                    temp = ""
    # TODO check potential non finished process paragraph/ overlap --accumulate all lines of a type?
    if p != "":
        process_paragraphs.append(p)
    elif temp != "":
        process_paragraphs.append(temp)

    for i, s in enumerate(process_paragraphs):
        process_paragraphs[i] = remove_linebreak_hyphen(s)

    return process_paragraphs


def preprocess_paragraphs(paragraphs: List[str]) -> List[str]:
    preprocessed_paragraphs = []
    for paragraph in paragraphs:
        preprocessed_paragraph = paragraph
        preprocessed_paragraph = fix_first_last_name_no_whitespace(
            preprocessed_paragraph
        )
        preprocessed_paragraph = (
            split_words_with_multiple_capital_characters_before_occupation(
                preprocessed_paragraph
            )
        )
        preprocessed_paragraph = add_missing_whitespace_before_occupation(
            preprocessed_paragraph
        )
        preprocess_paragraph = add_missing_whitespace_before_and_after_word_und(
            preprocessed_paragraph
        )
        preprocessed_paragraphs.append(preprocessed_paragraph)
    return preprocessed_paragraphs


def parse_segment(
    paragraph_as_dict: dict, process_paragraph: str, file_path: str, file_name: str
) -> dict:
    global invalid_process_checksum, valid_process_n, parsed_process_n, no_additional_data_person_n, processed_people
    p = process_paragraph
    d = paragraph_as_dict
    try:
        number_of_people = get_number_of_people_involved_in_process(p)
        first_names = get_first_name_of_people_involved_in_process(p)
        last_names = get_last_name_of_people_involved_in_process(p)
        occupations = get_occupation_of_people_involved_in_process(p)
        birthdays = get_birthday_of_people_involved_in_process(p)
        additional_person_data = get_additional_person_data(p)

        first_names_n = len(first_names)
        last_names_n = len(last_names)
        occupations_n = len(occupations)
        birthdays_n = len(birthdays)

        if (
            first_names_n != last_names_n
            or last_names_n != occupations_n
            or last_names_n != birthdays_n
        ):
            # segment might address more people/names, but they don't have to be mandatory accused of sth
            if False:
                print("---")
                print(f"{first_names=}")
                print(f"{last_names=}")
                print(f"{first_names_n}/{number_of_people}")
                print(f"{last_names_n}/{number_of_people}")
                print(zip(first_names, last_names))
                print(birthdays)
                print(p)
                print("---")
            raise ExtractProcessDataException

        d["Personen"] = [None] * last_names_n

        for i in range(last_names_n):
            d["Personen"][i] = {}
            first_name = first_names[i]
            last_name = last_names[i]
            d["Personen"][i]["Vorname"] = first_name
            d["Personen"][i]["Nachname"] = last_name
            d["Personen"][i]["Beruf"] = occupations[i]
            d["Personen"][i]["Geburtsdatum"] = birthdays[i]
            for p in additional_person_data:
                if p[0] == first_name and p[1] == last_name:
                    d["Personen"][i]["Zusatz"] = p[2]
                    break
            # TODO Urteil,Anlagen
        for i in range(last_names_n):
            if "Zusatz" not in d["Personen"][i]:
                d["Personen"][i]["Zusatz"] = None
                no_additional_data_person_n += 1
        valid_process_n += 1
        processed_people += last_names_n
    except ExtractProcessDataException:
        invalid_process_checksum += 1
        d = {}
    finally:
        parsed_process_n += 1
    return d


def text_segmentation_alg(file_path: str, file_name: str, id: str) -> List[dict]:
    global cwd, invalid_id_paragraph_n, valid_document_n, invalid_paragraph_segmentation_n, parsed_process_segements_n, missing_process_case_id_n
    """
    Return list with processes, empty list if document is invalid.
    Store invalid documents.
    """
    l = []
    try:
        old_ids = get_old_ids(file_path)
        new_ids = get_new_ids(file_path)

        if len(old_ids) == 0 or len(new_ids) == 0 or len(old_ids) != len(new_ids):
            raise InvalidIdParagraph

        process_paragraphs = parse_process_paragraphs(file_path, len(old_ids))
        process_paragraphs = preprocess_paragraphs(process_paragraphs)

        if len(process_paragraphs) != len(old_ids):
            raise ParagraphSegmentationException

        parsed_process_segements_n += len(process_paragraphs)

        for i, process_paragraph in enumerate(process_paragraphs):
            paragraph_as_dict = {
                "ID_Archiv_Alt": old_ids[i],
                "ID_Archiv_Neu": new_ids[i],
                "ID_Seite": id,
                "ID_Prozess": None,
                "Text": process_paragraph,
            }
            try:
                paragraph_as_dict["ID_Prozess"] = get_process_case_id(process_paragraph)
            except ProcessCaseIdException:
                if True:
                    print("\n", process_paragraph)  # process_paragraph[-40:]
                missing_process_case_id_n += 1

            paragraph_as_dict = parse_segment(
                paragraph_as_dict, process_paragraph, file_path, file_name
            )
            # check if dict is empty --exception was raised while parsing segments for the given paragraph
            if paragraph_as_dict:
                l.append(paragraph_as_dict)

        # end of "parser" -> no exception raised
        valid_document_n += 1

    except InvalidIdParagraph:
        invalid_id_paragraph_n += 1
    except ParagraphSegmentationException:
        invalid_paragraph_segmentation_n += 1
    return l


def exec_app():
    global invalid_process_checksum, missing_process_case_id_n, parsed_documents_n, invalid_document_name_n, invalid_id_paragraph_n, valid_document_n, invalid_paragraph_segmentation_n, parsed_process_n, valid_process_n, no_additional_data_person_n, processed_people
    d = {}
    d["Statistiken"] = {}
    d["Statistiken"]["Allgemein"] = {}
    d["Statistiken"]["Info_Ungültige_Dokumente"] = {}
    d["Dokumente"] = {}

    cwd = os.getcwd()
    path_txt = os.path.join(cwd, "text")
    Path(os.path.join(cwd, "output")).mkdir(parents=True, exist_ok=True)
    process_types = []

    for path, dir, files in os.walk(path_txt):
        process_types = dir
        break

    # [('/home/andreas/dh/text_to_json/text/Eingestellte_Verfahren', 'Eingestellte_Verfahren'), ...]
    process_paths_and_types = []  # (path,type)

    for type in process_types:
        process_paths_and_types.append((os.path.join(path_txt, type), type))
        d["Dokumente"][type] = []

    for (p, t) in process_paths_and_types:
        for path, dir, files in os.walk(p):
            # [('00118', '00118-NSJUSTIZ-BAND3-Teil_1-3_1_a_Prozesse_1934-20190129T163853l__PROCESSED.txt'), ...]
            ids_and_filenames = []  # (id,file)

            for file in files:
                try:
                    id = file[:5]

                    if not (len(id) == 5 and id.isdigit()):
                        raise InvalidDocumentName

                    ids_and_filenames.append((int(id), file))
                except InvalidDocumentName:
                    source = path + "/" + file
                    dest = os.path.join(
                        cwd, "output/invalid_documents/document_name/" + file
                    )
                    shutil.copyfile(source, dest)
                    invalid_document_name_n += 1
                finally:
                    parsed_documents_n += 1
            ids_and_filenames.sort(key=lambda x: x[0])
            d["Dokumente"][t] = []

            for (id, f) in ids_and_filenames:
                p_d_list = text_segmentation_alg(os.path.join(path, f), f, str(id))
                for p_d in p_d_list:
                    d["Dokumente"][t].append(p_d)

    # Add stats
    d["Statistiken"]["Allgemein"]["Gültige_Dokumente_Gesamt"] = valid_document_n
    d["Statistiken"]["Allgemein"]["Ungültige_Dokumente_Gesamt"] = (
        invalid_document_name_n
        + invalid_id_paragraph_n
        + invalid_paragraph_segmentation_n
    )
    d["Statistiken"]["Allgemein"]["Anzahl_Dokumente_Gesamt"] = (
        d["Statistiken"]["Allgemein"]["Gültige_Dokumente_Gesamt"]
        + d["Statistiken"]["Allgemein"]["Ungültige_Dokumente_Gesamt"]
    )
    d["Statistiken"]["Allgemein"][
        "Anzahl_Verarbeitete_Dokumente_Prüfsumme"
    ] = parsed_documents_n
    d["Statistiken"]["Allgemein"]["Anteil_Gültige_Dokumente"] = round(
        d["Statistiken"]["Allgemein"]["Gültige_Dokumente_Gesamt"]
        / d["Statistiken"]["Allgemein"]["Anzahl_Dokumente_Gesamt"],
        4,
    )
    d["Statistiken"]["Allgemein"]["Segmentierte_Prozesse"] = parsed_process_segements_n
    d["Statistiken"]["Allgemein"]["Prozesse_Parsed_Gesamt"] = parsed_process_n
    d["Statistiken"]["Allgemein"]["Gültige_Prozesse"] = valid_process_n
    d["Statistiken"]["Allgemein"]["Unültige_Prozesse"] = (
        parsed_process_n - valid_process_n
    )
    d["Statistiken"]["Allgemein"][
        "Unültige_Prozesse_Prüfsumme"
    ] = invalid_process_checksum
    d["Statistiken"]["Allgemein"]["Anteil_Gültige_Prozesse"] = round(
        valid_process_n / parsed_process_n, 4
    )
    d["Statistiken"]["Allgemein"]["Anzahl_Personen"] = processed_people

    # Add "invalid documents info"
    d["Statistiken"]["Info_Ungültige_Dokumente"][
        "Dokument_Name"
    ] = invalid_document_name_n
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Id_Absatz"] = invalid_id_paragraph_n
    d["Statistiken"]["Info_Ungültige_Dokumente"][
        "Process_Segmentierung"
    ] = invalid_paragraph_segmentation_n

    # data about missing values for given entries
    d["Statistiken"]["Info_None"] = {}
    d["Statistiken"]["Info_None"][
        "Prozess_ID"
    ] = f"{missing_process_case_id_n} ({round((missing_process_case_id_n/valid_process_n)*100,2)} %)"
    d["Statistiken"]["Info_None"][
        "Zusatz"
    ] = f"{no_additional_data_person_n} ({round((no_additional_data_person_n/processed_people)*100,2)} %)"

    with open(
        os.path.join(cwd, "output/output.json"), mode="w", encoding="utf-8"
    ) as fp:
        json.dump(d, fp, ensure_ascii=False)


if __name__ == "__main__":
    exec_app()
