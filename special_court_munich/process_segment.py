import re
import string

from nltk.tokenize import word_tokenize
from typing import List, Tuple, Optional
from datetime import datetime
from special_court_munich.corpus import CorpusStats


class ProcessCaseIdException(Exception):
    """Raised when the case id of the given process doesn't exist or can't be extracted."""

    def __init__(
        self,
        message="Raised when the case id of the given process doesn't exist or can't be extracted.",
    ):
        self.message = message
        super().__init__(self.message)


class ResultException(Exception):
    """Raised when the proceeding result doesn't exist or can't be extracted."""

    def __init__(
        self,
        message="Raised when the proceeding result doesn't exist or can't be extracted.",
    ):
        self.message = message
        super().__init__(self.message)


class AccusationException(Exception):
    """Raised when no accusation exist within a given proceeding or can't be extracted."""

    def __init__(
        self,
        message="Raised when no accusation exist within a given proceeding or can't be extracted.",
    ):
        self.message = message
        super().__init__(self.message)


class DurationException(Exception):
    """Raised when no proceeding duration exist within a given proceeding or can't be extracted."""

    def __init__(
        self,
        message="Raised when no proceeding duration exist within a given proceeding or can't be extracted.",
    ):
        self.message = message
        super().__init__(self.message)


class PeopleAttrMatchException(Exception):
    """Raised when number of first names, last names, occupations and birthdays do not add up."""

    pass


class MissingPeopleException(Exception):
    """Raised when no data about people can be extracted."""

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
    r"(?:den|die)\s?(?:jüdischen|jüdische|polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"((?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+)[A-ZÄÖÜ-]{3,}(?=[\s(,])"
)
pattern_last_name_person = re.compile(
    r"(?:den|die)\s?(?:jüdischen|jüdische|polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})(?=[\s(,])"
)
pattern_occupation_person = re.compile(
    r"(?:den|die)\s?(?:jüdischen|jüdische|polnischen|polnische)?\s?((?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?)\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+[A-ZÄÖÜ-]{3,}(?=[\s(,])"
)
pattern_birthday_person = re.compile(
    r"(?:[A-ZÄÖÜ][a-zäöü-]+\s)+[A-ZÄÖÜ-]{3,}"
    r"\s?[^\w\s]?\|?\s?\(\s?\w{1,3}(?:\s|\.|,)?\s?[^\w\s]?\|?\s?"
    r"(\d{1,2})(?:\s|\.|,)?\s?([JFMASOND][a-z]+)(?:\s|\.|,)?\s?(\d{4})\s?\)"
)
pattern_additional_person_data = re.compile(
    r"(?:den|die)\s?(?:jüdischen|jüdische|polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"((?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+)([A-ZÄÖÜ-]{3,})"
    r"\s?[^\w\s]?\|?\s?\(\s?\w{1,3}(?:\s|\.|,)?\s?[^\w\s]?\|?\s?\d{1,2}(?:\s|\.|,)?\s?[JFMASOND][a-z]+"
    r"(?:\s|\.|,)?\s?\d{4}\s?\)[\s,;]\s?([\w\s+)(.-]+?)\s?[\s,;]\s?(?=den|die|wegen)"
)

pattern_accusation_person = re.compile(
    r"(?=(?:den|die)\s?(?:jüdischen|jüdische|polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})"
    r".*(?:wegen|weil)\s?(.*)\.?\s?(?:Urteil|Verfahren).*)"
)

pattern_result_person = re.compile(
    r"(?=(?:den|die)\s?(?:jüdischen|jüdische|polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})"
    r".*((?:Urteil|Anklage|Verfahren).*?)(?:\(|\d{1,2}[,.]|Anlage))"
)

# 7. Nov. 1938 - 5. Dez. 1938
pattern_proceeding_duration = re.compile(
    r"((?:\s?\d{1,2}[.,]?\s?\w{3}[.,]?\s?\d{4}\s?\W?)+)(?<![)(])"
)

pattern_law_person = re.compile(
    r"(?=(?:den|die)\s?(?:jüdischen|jüdische|polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})"
    r".*Urteil.*(\(.*\))\s?\d{1,2}[.,]?)"
)

pattern_attachments_person = re.compile(
    r"(?=(?:den|die)\s?(?:jüdischen|jüdische|polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"[A-ZÄÖÜ][a-zäöü-]+(?:\sund\s[A-ZÄÖÜ][a-zäöü-]+)?\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+([A-ZÄÖÜ-]{3,})"
    r".*(Anlage.*?)(?:\(|\d{1,2}[,.]))"
)


pattern_parenthesis_content_post_birthday = re.compile(r"^.*\(.*\).*(\(.+\))\s?.*$")
# Teil 7 :: Register
pattern_document_name_duration = re.compile(
    r"^DHUP_NSJ_\d{5}_Band_3_Sondergericht_München_Teil_[123456]_(.*)_\d+\.(?:txt|hocr)$"
)

PUNCTUATION = string.punctuation

TYPE_PROZESS = ["Prozeß", "Frozeß"]
TYPE_ERMITTLUNGSVERFAHREN = ["Ermittlungsverfahren", "bErmittlungsverfahren"]


def get_proceeding_type(process_text: str) -> Optional[str]:
    line_mod = ""  # rm punctuation
    for c in process_text:
        if c not in PUNCTUATION:
            line_mod += c
    line_mod = line_mod.strip()
    words = word_tokenize(line_mod, language="german")
    if not words:
        return None
    if words[0] in TYPE_PROZESS:
        return "Prozeß"
    elif words[0] in TYPE_ERMITTLUNGSVERFAHREN:
        return "Ermittlunsgverfahren"
    else:
        return None


def get_duration(proceeding_text: str) -> str:
    durations = pattern_proceeding_duration.findall(proceeding_text)
    if durations:
        return durations[-1].strip()
    raise DurationException


def parse_process_segment(
    document_name: str,
    old_id: str,
    new_id: str,
    document_id,
    process_text: str,
    corpus_stats: CorpusStats = CorpusStats(),
    process_text_original: str = None,
) -> Tuple[dict, CorpusStats]:
    """Parse process segment into a structured format.

    Parameters:
        document_name (str): document name containing this proceeding.
        old_id (str): Old archive id from that process.
        new_id (str): New archive id from that process.
        document_id (str): Document (page) id.
        process_text (str): Text segment from that process.
        corpus_stats (CorpusStats): Current CorpusStats object --to be updated.
        process_text_original (str): Original text segment from that process.

    Returns:
        Tuple[dict, CorpusStats]: Revised version of the text segment.
    """
    p = process_text
    d = {
        "meta": {
            "page": document_id,
            "document_name": document_name,
            "type": get_proceeding_type(p),
            "processing_date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "error_tags": [],
        },
        "proceeding": {
            "ID": old_id,
            "shelfmark": new_id,
            "duration": None,
            "registration_no": None,
            "text_original": process_text_original,
            "text_preprocessed": process_text,
            "people": [],
        },
    }

    try:
        d["proceeding"]["duration"] = get_duration(process_text)
    except DurationException:
        d["meta"]["error_tags"].append("missing_duration")

    try:
        d["proceeding"]["registration_no"] = get_registration_no(process_text)
    except ProcessCaseIdException:
        d["meta"]["error_tags"].append("missing_registration_no")
        # print("\n", process_paragraph)  # process_paragraph[-40:]

    if not d["proceeding"]["ID"]:
        d["meta"]["error_tags"].append("missing_ID")
    if not d["proceeding"]["shelfmark"]:
        d["meta"]["error_tags"].append("missing_shelfmark")

    try:
        number_of_people = get_number_of_people_involved_in_process(p)
        first_names = get_first_name_of_people_involved_in_process(p)
        last_names = get_last_name_of_people_involved_in_process(p)
        occupations = get_occupation_of_people_involved_in_process(p)
        birthdays = get_birthday_of_people_involved_in_process(p)
        additional_person_data = get_additional_person_data(p)
        attachments_person_data = get_attachments(p)
        law_person_data = get_law(p)
        accusation_person_data = None
        result_person_data = None

        try:
            accusation_person_data = get_accusations(p)
        except AccusationException:
            d["meta"]["error_tags"].append("missing_accusation")
        try:
            result_person_data = get_result(p)
        except ResultException:
            d["meta"]["error_tags"].append("missing_result")

        first_names_n = len(first_names)
        last_names_n = len(last_names)
        occupations_n = len(occupations)
        birthdays_n = len(birthdays)

        if first_names_n == 0 or (first_names_n != last_names_n):
            # segment might address more people/names, but they don't have to be mandatory accused of sth
            # TODO
            """
            if (
                (first_names_n == last_names_n)
                and (last_names_n == occupations_n)
                and first_names_n == 1
            ):
                print(first_names_n, last_names_n, occupations_n, birthdays_n)
                print(p)
                print("")
            """
            raise MissingPeopleException

        d["proceeding"]["people"] = [{} for _ in range(last_names_n)]

        for i in range(last_names_n):
            corpus_stats.inc_val_persons()
            first_name = first_names[i]
            last_name = last_names[i]
            d["proceeding"]["people"][i]["first_name"] = first_name
            d["proceeding"]["people"][i]["last_name"] = last_name
            d["proceeding"]["people"][i]["occupation"] = None
            if first_names_n == occupations_n:
                d["proceeding"]["people"][i]["occupation"] = occupations[i]
            else:
                if "missing_occupation" not in d["meta"]["error_tags"]:
                    d["meta"]["error_tags"].append("missing_occupation")
            d["proceeding"]["people"][i]["date_of_birth"] = None
            if first_names_n == birthdays_n:
                d["proceeding"]["people"][i]["date_of_birth"] = birthdays[i]
            else:
                if "missing_date_of_birth" not in d["meta"]["error_tags"]:
                    d["meta"]["error_tags"].append("missing_date_of_birth")
            d["proceeding"]["people"][i]["accusation"] = None
            d["proceeding"]["people"][i]["law"] = None
            d["proceeding"]["people"][i]["result"] = None
            d["proceeding"]["people"][i]["residence"] = None
            d["proceeding"]["people"][i]["attachements"] = None
            d["proceeding"]["people"][i]["add_prosecution"] = None  # TODO
            # add residence
            for p in additional_person_data:
                if p[0] == first_name and p[1] == last_name:
                    if p[2].strip().split()[0] == "aus":
                        d["proceeding"]["people"][i]["residence"] = p[2].lstrip("aus ")
                    break
            # add accusations
            if accusation_person_data:
                for name, accusation in accusation_person_data:
                    if name == last_name:
                        d["proceeding"]["people"][i]["accusation"] = accusation

            # add result
            if result_person_data:
                for name, result in result_person_data:
                    if name == last_name:
                        d["proceeding"]["people"][i]["result"] = result
            # add alw
            if law_person_data:
                for name, law in law_person_data:
                    if name == last_name:
                        d["proceeding"]["people"][i]["law"] = law
            # add attachments
            if attachments_person_data:
                for name, attachments in law_person_data:
                    if name == last_name:
                        d["proceeding"]["people"][i]["attachments"] = attachments
        # valid :: people attr with content
        corpus_stats.inc_val_valid_proceedings()
    except MissingPeopleException:
        # missing people data
        d["meta"]["error_tags"].append("missing_people")
    finally:
        if d:
            if d["proceeding"]["registration_no"]:
                # increment, iff parsing the process segment did not raise an exception and contains process id
                corpus_stats.inc_val_valid_registration_no()
        corpus_stats.inc_val_parsed_proceedings()
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
    # TODO reduce complexity by considering only process segments with one person
    additional_person_data = pattern_additional_person_data.findall(process_text)
    additional_person_data = [
        (x.strip(), y.strip(), z.strip())
        for (x, y, z) in additional_person_data
        if z != "und"
    ]
    number_people_involved = get_number_of_people_involved_in_process(process_text)
    if number_people_involved == 2:
        replacement = None
        for data in [z for (x, y, z) in additional_person_data]:
            if "beide aus" in data or "beideaus" in data:
                replacement = data.replace("beide", "").strip()
        if replacement:
            first_names = get_first_name_of_people_involved_in_process(process_text)
            last_names = get_last_name_of_people_involved_in_process(process_text)
            additional_person_data = [
                (x, y, replacement) for (x, y) in zip(first_names, last_names)
            ]
    elif number_people_involved > 2:
        replacement = None
        for data in [z for (x, y, z) in additional_person_data]:
            if "alle aus" in data or "alleaus" in data:
                replacement = data.replace("alle", "").strip()
        if replacement:
            first_names = get_first_name_of_people_involved_in_process(process_text)
            last_names = get_last_name_of_people_involved_in_process(process_text)
            additional_person_data = [
                (x, y, replacement) for (x, y) in zip(first_names, last_names)
            ]
    return additional_person_data


def get_registration_no(process_text: str) -> str:
    """Extract registration number out of paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        str: registration number.

    Raises:
        ProcessIdException - Raised when the registration number can't be extracted.
    """
    registration_no = pattern_parenthesis_content_post_birthday.findall(process_text)
    if registration_no:
        # assume last parenthesis stack post birthday is registration number
        check_registration_no = registration_no[-1]
        if "geb" in check_registration_no:
            raise ProcessCaseIdException
        else:
            return check_registration_no
    else:
        raise ProcessCaseIdException


def get_accusations(process_text: str) -> List[Tuple[str, str]]:
    """Extract accusation data on persons mentioned in the paragraph segment.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[Tuple[str, str]]: List of people and the corresponding accusation.

    Raises:
        AccusationException - Raised when no accusation exist within a given proceeding or can't be extracted.
    """
    people_accusations = pattern_accusation_person.findall(process_text)
    if people_accusations:
        return [(n, a.strip().rstrip(".")) for n, a in people_accusations]
    raise AccusationException


def get_result(process_text: str) -> List[Tuple[str, str]]:
    """Extract the result of a proceeding.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[Tuple[str, str]]: List of people and the corresponding proceeding result.

    Raises:
        ResultException - Raised when the proceeding result doesn't exist or can't be extracted.
    """
    people_results = pattern_result_person.findall(process_text)
    if people_results:
        return [(n, a.strip().rstrip(".")) for n, a in people_results]
    raise ResultException


def get_law(process_text: str) -> List[Tuple[str, str]]:
    """Extract the law attributes of a proceeding.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[Tuple[str, str]]: List of people and the corresponding law attribute related to the result.

    Raises:
        ResultException - Raised when a law attribute doesn't exist or can't be extracted.
    """
    people_law = pattern_law_person.findall(process_text)
    return [(n, a.strip()) for n, a in people_law]


def get_attachments(process_text: str) -> List[Tuple[str, str]]:
    """Extract the attachments of a proceeding.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        List[Tuple[str, str]]: List of people and the corresponding attachments.

    Raises:
        ResultException - Raised when attachments do not exist or can not be extracted.
    """
    people_attachments = pattern_attachments_person.findall(process_text)
    return [(n, a.strip()) for n, a in people_attachments]
