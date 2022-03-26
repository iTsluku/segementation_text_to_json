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
    """Raised when the case id of the given process doesn't exist or can't be extracted."""

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
