import os
import json

from ocr import PreprocessSegment
from ocr import ProcessSegment
from pathlib import Path
from typing import List

from ocr.CorpusStats import CorpusStats

cwd = os.getcwd()
corpus_stats = CorpusStats()


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
        preprocessed_paragraph = PreprocessSegment.fix_first_last_name_no_whitespace(
            preprocessed_paragraph
        )
        preprocessed_paragraph = PreprocessSegment.split_words_with_multiple_capital_characters_before_occupation(
            preprocessed_paragraph
        )
        preprocessed_paragraph = (
            PreprocessSegment.add_missing_whitespace_before_occupation(
                preprocessed_paragraph
            )
        )
        preprocessed_paragraph = (
            PreprocessSegment.add_missing_whitespace_before_and_after_word_und(
                preprocessed_paragraph
            )
        )
        preprocessed_paragraphs.append(preprocessed_paragraph)
    return preprocessed_paragraphs


def parse_segment(
    paragraph_as_dict: dict, process_paragraph: str, file_path: str, file_name: str
) -> dict:
    p = process_paragraph
    d = paragraph_as_dict
    try:
        number_of_people = ProcessSegment.get_number_of_people_involved_in_process(p)
        first_names = ProcessSegment.get_first_name_of_people_involved_in_process(p)
        last_names = ProcessSegment.get_last_name_of_people_involved_in_process(p)
        occupations = ProcessSegment.get_occupation_of_people_involved_in_process(p)
        birthdays = ProcessSegment.get_birthday_of_people_involved_in_process(p)
        additional_person_data = ProcessSegment.get_additional_person_data(p)

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
            """if
            print("---")
            print(f"{first_names=}")
            print(f"{last_names=}")
            print(f"{first_names_n}/{number_of_people}")
            print(f"{last_names_n}/{number_of_people}")
            print(zip(first_names, last_names))
            print(birthdays)
            print(p)
            print("---")
            """
            raise ExtractProcessDataException

        d["Personen"] = [None] * last_names_n

        for i in range(last_names_n):
            corpus_stats.inc_val_people()
            d["Personen"][i] = {}
            first_name = first_names[i]
            last_name = last_names[i]
            d["Personen"][i]["Vorname"] = first_name
            d["Personen"][i]["Nachname"] = last_name
            d["Personen"][i]["Beruf"] = occupations[i]
            d["Personen"][i]["Geburtsdatum"] = birthdays[i]
            d["Personen"][i]["Zusatz"] = None
            for p in additional_person_data:
                if p[0] == first_name and p[1] == last_name:
                    d["Personen"][i]["Zusatz"] = p[2]
                    corpus_stats.inc_val_people_add_data()
                    break
            # TODO Urteil,Anlagen
        corpus_stats.inc_val_valid_processes()
    except ExtractProcessDataException:
        d = {}
    finally:
        corpus_stats.inc_parsed_processes()
    return d


def text_segmentation_alg(file_path: str, file_name: str, id: str) -> List[dict]:
    """
    Return list with processes, empty list if document is invalid.
    """
    process_paragraphs_dict_list = []
    try:
        old_ids = get_old_ids(file_path)
        new_ids = get_new_ids(file_path)

        if len(old_ids) == 0 or len(new_ids) == 0 or len(old_ids) != len(new_ids):
            raise InvalidIdParagraph

        process_paragraphs = parse_process_paragraphs(file_path, len(old_ids))
        process_paragraphs = preprocess_paragraphs(process_paragraphs)

        if len(process_paragraphs) != len(old_ids):
            raise ParagraphSegmentationException

        for i, process_paragraph in enumerate(process_paragraphs):
            paragraph_as_dict = {
                "ID_Archiv_Alt": old_ids[i],
                "ID_Archiv_Neu": new_ids[i],
                "ID_Seite": id,
                "ID_Prozess": None,
                "Text": process_paragraph,
            }

            try:
                paragraph_as_dict["ID_Prozess"] = ProcessSegment.get_process_case_id(
                    process_paragraph
                )
            except ProcessSegment.ProcessCaseIdException:
                pass
                # print("\n", process_paragraph)  # process_paragraph[-40:]

            paragraph_as_dict = parse_segment(
                paragraph_as_dict, process_paragraph, file_path, file_name
            )
            # check if dict is empty --exception was raised while parsing segments for the given paragraph
            if paragraph_as_dict:
                process_paragraphs_dict_list.append(paragraph_as_dict)
                if paragraph_as_dict["ID_Prozess"]:
                    corpus_stats.inc_val_valid_process_ids()

        # end of "parser" -> no exception raised
        corpus_stats.inc_val_valid_docs()

    except InvalidIdParagraph:
        pass
    except ParagraphSegmentationException:
        pass
    return process_paragraphs_dict_list


def main():
    dictionary = {"CorpusStats": {}, "Dokumente": {}}
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
        dictionary["Dokumente"][type] = []

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
                    pass
                finally:
                    corpus_stats.inc_val_parsed_docs()
            ids_and_filenames.sort(key=lambda x: x[0])
            dictionary["Dokumente"][t] = []

            for (id, f) in ids_and_filenames:
                p_d_list = text_segmentation_alg(os.path.join(path, f), f, str(id))
                for p_d in p_d_list:
                    dictionary["Dokumente"][t].append(p_d)
    dictionary["CorpusStats"] = corpus_stats.get_repr_dict()
    with open(
        os.path.join(cwd, "output/output.json"), mode="w", encoding="utf-8"
    ) as fp:
        json.dump(dictionary, fp, ensure_ascii=False)


if __name__ == "__main__":
    main()
