import re


class GroupingIndex(object):
    def __init__(self, items, start_index=0):
        self.index = start_index - 1
        self.items = items

    def __call__(self, match):
        self.index += 1
        return self.items[self.index]


def fix_first_last_name_no_whitespace(text: str) -> str:
    pattern_first_second_name_no_whitespace = re.compile(
        r"([A-ZÄÖÜ][a-zäöü]+)([A-ZÄÖÜ-]{3,})(?=[\s(,])"
    )
    pattern_first_second_name_no_whitespace_together = re.compile(
        r"([A-ZÄÖÜ][a-zäöü]+[A-ZÄÖÜ-]{3,})(?=[\s(,])"
    )
    name_groupings = pattern_first_second_name_no_whitespace.findall(text)
    replacements = [f"{x} {y}" for (x, y) in name_groupings]
    output = text
    output = pattern_first_second_name_no_whitespace_together.sub(
        GroupingIndex(replacements),
        output,
    )
    return output


def split_words_with_multiple_capital_characters_before_occupation(
    process_text: str,
) -> str:
    a_b_sep = re.compile(
        r"([A-ZÄÖÜ-][a-zäöü-]+)([A-ZÄÖÜ-][a-zäöü-]+)(?=\s[A-ZÄÖÜ-]{3,})"
    )
    a_and_b = re.compile(r"([A-ZÄÖÜ-][a-zäöü-]+[A-ZÄÖÜ-][a-zäöü-]+)(?=\s[A-ZÄÖÜ-]{3,})")
    name_groupings = a_b_sep.findall(process_text)
    replacements = [f"{x} {y}" for (x, y) in name_groupings]
    output = process_text
    output = a_and_b.sub(
        GroupingIndex(replacements),
        output,
    )
    return output
