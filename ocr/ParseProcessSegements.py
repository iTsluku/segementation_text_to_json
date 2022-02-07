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

pattern_person = re.compile(r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})(?=[\s(,])")
pattern_first_name_person = re.compile(
    r"(?:den|die)\s?[A-ZÄÖÜ][a-zäöü-]+\s((?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+)[A-ZÄÖÜ-]{3,}(?=[\s(,])"
)
pattern_last_name_person = re.compile(
    r"(?:den|die)\s?[A-ZÄÖÜ][a-zäöü-]+\s(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})(?=[\s(,])"
)
pattern_occupation_person = re.compile(
    r"(?:den|die)\s?([A-ZÄÖÜ][a-zäöü-]+)\s(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+[A-ZÄÖÜ-]{3,}(?=[\s(,])"
)
pattern_birthday_person = re.compile(
    r"(?:[A-ZÄÖÜ][a-zäöü-]+\s)+[A-ZÄÖÜ-]{3,}"
    r"\s?\(\s?\w{3}(?:\s|\.)?\s?(\d{1,2})(?:\s|\.)?\s?([JFMASOND][a-z]+)(?:\s|\.)?\s?(\d{4})\s?\)"
)


def get_number_of_persons_involved_in_process(paragraph_text: str) -> int:
    person_groupings = pattern_person.findall(paragraph_text)
    return len(person_groupings)


def get_first_name_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
    # remove ending whitespace
    return [x[:-1] for x in pattern_first_name_person.findall(paragraph_text)]


def get_last_name_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
    return pattern_last_name_person.findall(paragraph_text)


def get_occupation_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
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


def get_birthday_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
    birthdays = pattern_birthday_person.findall(paragraph_text)
    return parse_birthday_tuples(birthdays)
