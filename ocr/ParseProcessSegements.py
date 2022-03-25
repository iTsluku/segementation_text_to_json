import re

from typing import List, Tuple

"""assumptions
    last name >=3 chars
    char :: [',',' ','('] after last name (-> not ['-',...])
    "den " or "die " prefix before occupation :: (den|die) <occupation> first_name+ LAST_NAME
"""
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


class Error(Exception):
    """Base class for other exceptions."""

    pass


class ProcessCaseIdException(Error):
    def __init__(
        self,
        message="Raised when the case id of the given process doesn't exist or can't be extracted.",
    ):
        self.message = message
        super().__init__(self.message)


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


def get_number_of_people_involved_in_process(paragraph_text: str) -> int:
    person_groupings = pattern_person.findall(paragraph_text)
    return len(person_groupings)


def get_first_name_of_people_involved_in_process(paragraph_text: str) -> List[str]:
    # remove ending whitespace
    return [x.rstrip() for x in pattern_first_name_person.findall(paragraph_text)]


def get_last_name_of_people_involved_in_process(paragraph_text: str) -> List[str]:
    return pattern_last_name_person.findall(paragraph_text)


def get_occupation_of_people_involved_in_process(paragraph_text: str) -> List[str]:
    return pattern_occupation_person.findall(paragraph_text)


def parse_birthday_tuples(birthdays: List[Tuple[str, str, str]]) -> List[str]:
    # YYYY-MM-DD
    formatted_birthdays = []
    for t in birthdays:
        if len(t[0]) == 1:
            day = "0" + t[0]
        else:
            day = t[0]
        if t[1] in month_number:
            formatted_birthdays.append(f"{t[2]}-{month_number[t[1]]}-{day}")
    return formatted_birthdays


def get_birthday_of_people_involved_in_process(paragraph_text: str) -> List[str]:
    birthdays = pattern_birthday_person.findall(paragraph_text)
    return parse_birthday_tuples(birthdays)


def get_additional_person_data(paragraph_text: str) -> List[Tuple[str, str, str]]:
    additional_person_data = pattern_additional_person_data.findall(paragraph_text)
    return [(x.strip(), y.strip(), z.strip()) for (x, y, z) in additional_person_data]


def get_process_case_id(paragraph_text: str) -> str:
    """Extract process id out of paragraph segment.

    Returns:
        str: process id.
    Raises:
        ProcessIdException - Raised when the process id can't be extracted.
    """
    process_id = pattern_process_case_id.findall(paragraph_text)
    if process_id:
        return process_id[0]
    else:
        raise ProcessCaseIdException
