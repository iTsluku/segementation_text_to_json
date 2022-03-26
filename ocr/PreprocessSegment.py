import re

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
