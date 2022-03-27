import re

from typing import List

pattern_first_second_name_no_whitespace = re.compile(
    r"([A-ZÄÖÜ][a-zäöü]+)([A-ZÄÖÜ-]{3,})(?=[\s(,])"
)
pattern_first_second_name_no_whitespace_together = re.compile(
    r"([A-ZÄÖÜ][a-zäöü]+[A-ZÄÖÜ-]{3,})(?=[\s(,])"
)
pattern_pre_occupation_no_whitespace_separated = re.compile(
    r"([A-ZÄÖÜ-][a-zäöü-]+)([A-ZÄÖÜ-][a-zäöü-]+)(?=\s[A-ZÄÖÜ-]{3,})"
)
pattern_pre_occupation_no_whitespace_together = re.compile(
    r"([A-ZÄÖÜ-][a-zäöü-]+[A-ZÄÖÜ-][a-zäöü-]+)(?=\s[A-ZÄÖÜ-]{3,})"
)

pattern_occupation_prefix_missing_whitespace = re.compile(
    r"^(?:den|die)[A-ZÄÖÜ-][a-zäöü-]+$"
)
pattern_occupation_and_word_und_missing_whitespace = re.compile(
    r"(?:den|die)\s?(?:polnischen|polnische)?\s?(?:ldw.|kath.|kfm.|landw.)?\s?"
    r"((?:[A-ZÄÖÜ][a-zäöü-]+und\s[A-ZÄÖÜ][a-zäöü-]+)|(?:[A-ZÄÖÜ][a-zäöü-]+\sund[A-ZÄÖÜ][a-zäöü-]+)|"
    r"(?:[A-ZÄÖÜ][a-zäöü-]+und[A-ZÄÖÜ][a-zäöü-]+))\s"
    r"(?:(?:[A-ZÄÖÜ][a-zäöü-]+)+\s)+[A-ZÄÖÜ-]{3,}(?=[\s(,])"
)


class GroupingIndex(object):
    def __init__(self, items, start_index=0):
        self.index = start_index - 1
        self.items = items

    def __call__(self, match):
        self.index += 1
        return self.items[self.index]


def fix_first_last_name_no_whitespace(process_text: str) -> str:
    """Add missing whitespace between first and last name.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        str: Revised version of the process text segment.
    """
    name_groupings = pattern_first_second_name_no_whitespace.findall(process_text)
    replacements = [f"{x} {y}" for (x, y) in name_groupings]
    output = process_text
    output = pattern_first_second_name_no_whitespace_together.sub(
        GroupingIndex(replacements),
        output,
    )
    return output


def split_words_with_multiple_capital_characters_before_occupation(
    process_text: str,
) -> str:
    """Add missing whitespace before occupation.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        str: Revised version of the process text segment.
    """
    name_groupings = pattern_pre_occupation_no_whitespace_separated.findall(
        process_text
    )
    replacements = [f"{x} {y}" for (x, y) in name_groupings]
    output = process_text
    output = pattern_pre_occupation_no_whitespace_together.sub(
        GroupingIndex(replacements),
        output,
    )
    return output


def add_missing_whitespace_before_occupation(process_text: str) -> str:
    """Add missing whitespace after keywords ["den","die"] - before occupation.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        str: Revised version of the process text segment.
    """
    processed_words = []
    for word in process_text.split():
        p = pattern_occupation_prefix_missing_whitespace.match(word)
        if p:
            processed_words.append(word[:3] + " " + word[3:])
        else:
            processed_words.append(word)
    return " ".join(processed_words)


def add_missing_whitespace_before_and_after_word_und(process_text: str) -> str:
    """Add the missing space before and after the keyword "and" within the segment for the occurrence of 2 professions.

    Parameters:
        process_text (str): Process text segment.

    Returns:
        str: Revised version of the process text segment.
    """
    processed_words = []
    missing_whitespace_cases = (
        pattern_occupation_and_word_und_missing_whitespace.findall(process_text)
    )
    missing_whitespace_cases_processed = []
    for word in missing_whitespace_cases:
        words = word.split()
        for w in words:
            if "und" in w:
                missing_whitespace_cases_processed.append(w)
                break
    for word in process_text.split():
        if "und" in word and word in missing_whitespace_cases_processed:
            tokens = word.split("und")
            if tokens[0] == "":
                word_processed = "und"
            else:
                word_processed = tokens[0] + " und"
            if tokens[1] != "":
                word_processed += " " + tokens[1]
            processed_words.append(word_processed)
        else:
            processed_words.append(word)
    return " ".join(processed_words)


def remove_linebreak_hyphen(line: str) -> str:
    """Remove hyphen if it is followed by a line break, when line processing a document.

    Parameters:
        line (str): Line of a document.

    Returns:
        str: Revised version of the text segment.
    """
    o = ""
    prev = ""

    for c in line:
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


def preprocess_processes(processes: List[str]) -> List[str]:
    """Apply a pipeline of preprocessing functions to given processes.

    Parameters:
        processes (List[str]): List of process text segments.

    Returns:
        List[str]: Revised text version of processes.
    """
    preprocessed_processes = []
    for process_text in processes:
        preprocessed_process_text = process_text
        preprocessed_process_text = fix_first_last_name_no_whitespace(
            preprocessed_process_text
        )
        preprocessed_process_text = (
            split_words_with_multiple_capital_characters_before_occupation(
                preprocessed_process_text
            )
        )
        preprocessed_process_text = add_missing_whitespace_before_occupation(
            preprocessed_process_text
        )
        preprocessed_process_text = add_missing_whitespace_before_and_after_word_und(
            preprocessed_process_text
        )
        preprocessed_processes.append(preprocessed_process_text)
    return preprocessed_processes
