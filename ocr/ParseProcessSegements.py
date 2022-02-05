import re

from typing import List


def get_number_of_persons_involved_in_process(paragraph_text: str) -> int:
    # assume: last name >=3 chars
    pattern_person = re.compile(r"([A-ZÄÖU][a-zäöü]+\s[A-ZÄÖÜ]{3,})")
    person_groupings = pattern_person.findall(paragraph_text)
    return len(person_groupings)


def get_first_name_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
    # assume: last name >=3 chars
    # TODO last name ending condition/look-ahead
    pattern_first_name_person = re.compile(r"([A-ZÄÖU][a-zäöü]+)\s[A-ZÄÖÜ]{3,}")
    return pattern_first_name_person.findall(paragraph_text)


def get_last_name_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
    # assume: last name >=3 chars
    # TODO last name ending condition/look-ahead
    pattern_first_name_person = re.compile(r"[A-ZÄÖU][a-zäöü]+\s([A-ZÄÖÜ]{3,})")
    return pattern_first_name_person.findall(paragraph_text)
