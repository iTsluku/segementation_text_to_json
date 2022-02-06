import re

from typing import List

"""assumptions
    last name >=3 chars
    char :: [',',' ','('] after last name (-> not ['-',...])
    "den " or "die " prefix before occupation :: (den|die) <occupation> first_name+ LAST_NAME
"""


def get_number_of_persons_involved_in_process(paragraph_text: str) -> int:
    pattern_person = re.compile(
        r"[\s,](?:den|die)\s([A-ZÄÖÜ][a-zäöü-]+)\s(?:(?:[A-ZÄÖÜ][a-zäöü-]+\s)+)[A-ZÄÖÜ-]{3,}(?=[\s(,])"
    )
    person_groupings = pattern_person.findall(paragraph_text)
    return len(person_groupings)


def get_first_name_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
    pattern_first_name_person = re.compile(
        r"[\s,](?:den|die)\s[A-ZÄÖÜ][a-zäöü-]+\s((?:[A-ZÄÖÜ][a-zäöü-]+\s)+)[A-ZÄÖÜ-]{3,}(?=[\s(,])"
    )
    # remove ending whitespace
    return [x[:-1] for x in pattern_first_name_person.findall(paragraph_text)]


def get_last_name_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
    pattern_first_name_person = re.compile(
        r"[\s,](?:den|die)\s[A-ZÄÖÜ][a-zäöü-]+\s(?:(?:[A-ZÄÖÜ][a-zäöü-]+\s)+)([A-ZÄÖÜ-]{3,})(?=[\s(,])"
    )
    return pattern_first_name_person.findall(paragraph_text)


def get_occupation_of_persons_involved_in_process(paragraph_text: str) -> List[str]:
    pattern_occupation_person = re.compile(
        r"[\s,](?:den|die)\s([A-ZÄÖÜ][a-zäöü-]+)\s(?:(?:[A-ZÄÖÜ][a-zäöü-]+\s)+)[A-ZÄÖÜ-]{3,}(?=[\s(,])"
    )
    return pattern_occupation_person.findall(paragraph_text)
