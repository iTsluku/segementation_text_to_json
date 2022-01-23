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
        r"([A-ZÄÖU][a-zäöü]+)([A-ZÄÖÜ]+)"
    )
    pattern_first_second_name_no_whitespace_together = re.compile(
        r"([A-ZÄÖU][a-zäöü]+[A-ZÄÖÜ]+)"
    )
    name_groupings = re.findall(pattern_first_second_name_no_whitespace, text)
    replacements = [f"{x} {y}" for (x, y) in name_groupings]
    output = text
    output = re.sub(
        pattern_first_second_name_no_whitespace_together,
        GroupingIndex(replacements),
        output,
    )
    return output
