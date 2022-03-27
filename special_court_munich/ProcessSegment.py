import re

from typing import List, Tuple
from special_court_munich.CorpusStats import CorpusStats


class ProcessCaseIdException(Exception):
    """Raised when the case id of the given process doesn't exist or can't be extracted."""

    def __init__(
        self,
        message="Raised when the case id of the given process doesn't exist or can't be extracted.",
    ):
        self.message = message
        super().__init__(self.message)


class ExtractProcessDataException(Exception):
    """Raised when number of first names, last names or occupations don't add up"""

    pass


month_number = {
    "Jan": "01",
    "Feb": "02",
    "Mrz": "03",
    "Apr": "04",
    "Mai": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Spt": "09",
    "Okt": "10",
    "Nov": "11",
    "Dez": "12",
}
pattern_person = re.compile(r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})(?=[\s(,])")
pattern_first_name_person = re.compile(
    r"(?:den|die)\s?(?:polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"((?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+)[A-ZÄÖÜ-]{3,}(?=[\s(,])"
)
pattern_last_name_person = re.compile(
    r"(?:den|die)\s?(?:polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})(?=[\s(,])"
)
pattern_occupation_person = re.compile(
    r"(?:den|die)\s?(?:polnischen|polnische)?\s?((?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?)\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+[A-ZÄÖÜ-]{3,}(?=[\s(,])"
)
pattern_birthday_person = re.compile(
    r"(?:[A-ZÄÖÜ][a-zäöü-]+\s)+[A-ZÄÖÜ-]{3,}"
    r"\s?\(\s?\w{1,3}(?:\s|\.|,)?\s?(\d{1,2})(?:\s|\.|,)?\s?([JFMASOND][a-z]+)(?:\s|\.|,)?\s?(\d{4})\s?\)"
)
pattern_additional_person_data = re.compile(
    r"(?:den|die)\s?(?:polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"((?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+)([A-ZÄÖÜ-]{3,})"
    r"\s?\(\s?\w{1,3}(?:\s|\.|,)?\s?\d{1,2}(?:\s|\.|,)?\s?[JFMASOND][a-z]+(?:\s|\.|,)?\s?\d{4}\s?\)"
    r"[\s,;]\s?([\w\s+)(.-]+?)\s?[\s,;]\s?(?=den|die|wegen)"
)

pattern_process_case_id = re.compile(r"\(([?:<>$,;\w\d\s/-]+)\)?\s?[‘.,;|]?$")


def parse_process_segment(
    old_id: str, new_id: str, document_id, process_text: str, corpus_stats=CorpusStats()
) -> Tuple[dict, CorpusStats]:
    """Parse process segment into a structured format.

    Parameters:
        old_id (str): Old archive id from that process.
        new_id (str): New archive id from that process.
        document_id (str): Document (page) id.
        process_text (str): Text segment from that process.
        corpus_stats (CorpusStats): Current CorpusStats object --to be updated.

    Returns:
        Tuple[dict, CorpusStats]: Revised version of the text segment.
    """
    p = process_text
    d = {
        "ID_Archiv_Alt": old_id,
        "ID_Archiv_Neu": new_id,
        "ID_Seite": document_id,
        "ID_Prozess": None,
        "Text": process_text,
    }

    try:
        d["ID_Prozess"] = get_process_case_id(process_text)
    except ProcessCaseIdException:
        pass
        # print("\n", process_paragraph)  # process_paragraph[-40:]
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

        d["Personen"] = [{}] * last_names_n

        for i in range(last_names_n):
            corpus_stats.inc_val_people()
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
        if d:
            if d["ID_Prozess"]:
                # increment, iff parsing the process segment did not raise an exception and contains process id
                corpus_stats.inc_val_valid_process_ids()
        corpus_stats.inc_val_parsed_processes()
        return d, corpus_stats


def get_number_of_people_involved_in_process(process_text: str) -> int:
    """Extract number of convicted persons mentioned in the paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        int: Number of convicted persons.
    """
    person_groupings = pattern_person.findall(process_text)
    return len(person_groupings)


def get_first_name_of_people_involved_in_process(process_text: str) -> List[str]:
    """Extract first names of people mentioned in the paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[str]: List of first names.
    """
    # remove ending whitespace
    return [x.rstrip() for x in pattern_first_name_person.findall(process_text)]


def get_last_name_of_people_involved_in_process(process_text: str) -> List[str]:
    """Extract last names of people mentioned in the paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[str]: List of last names.
    """
    return pattern_last_name_person.findall(process_text)


def get_occupation_of_people_involved_in_process(process_text: str) -> List[str]:
    """Extract occupations of people mentioned in the paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[str]: List of occupations.
    """
    return pattern_occupation_person.findall(process_text)


def parse_birthday_tuples(birthdays: List[Tuple[str, str, str]]) -> List[str]:
    """Format birthdays.

    Parameters:
        birthdays (List[Tuple[str, str, str]]): List of birthdays.

    Returns:
        List[str]: List of YYYY-MM-DD formatted birthdays.
    """
    formatted_birthdays = []
    for t in birthdays:
        if len(t[0]) == 1:
            day = "0" + t[0]
        else:
            day = t[0]
        if t[1] in month_number:
            formatted_birthdays.append(f"{t[2]}-{month_number[t[1]]}-{day}")
    return formatted_birthdays


def get_birthday_of_people_involved_in_process(process_text: str) -> List[str]:
    """Extract birthdays of people mentioned in the paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[str]: List of formatted birthdays.
    """
    birthdays = pattern_birthday_person.findall(process_text)
    return parse_birthday_tuples(birthdays)


def get_additional_person_data(process_text: str) -> List[Tuple[str, str, str]]:
    """Extract additional data on persons mentioned in the paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[Tuple[str, str, str]]: List of people by first name, last name and additional data.
    """
    additional_person_data = pattern_additional_person_data.findall(process_text)
    return [(x.strip(), y.strip(), z.strip()) for (x, y, z) in additional_person_data]


def get_process_case_id(process_text: str) -> str:
    """Extract process id out of paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        str: process id.

    Raises:
        ProcessIdException - Raised when the process id can't be extracted.
    """
    process_id = pattern_process_case_id.findall(process_text)
    if process_id:
        return process_id[0]
    else:
        raise ProcessCaseIdException
