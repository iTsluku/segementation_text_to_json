from typing import List


def get_old_ids(file_path: str) -> List[str]:
    old_ids = []

    with open(file_path) as f:
        for line in f:
            if line not in ["\n", "\r\n", ""]:
                line = line.strip().replace(".", "")
                if line[0] == "(" and line[-1] == ")":
                    line = line.replace("(", "").replace(")", "")
                    if line.isdigit() and len(line) >= 3:
                        old_ids.append(line)
                else:
                    break
    return old_ids


def get_new_ids(file_path: str) -> List[str]:
    new_ids = []

    with open(file_path) as f:
        for line in f:
            if line not in ["\n", "\r\n", ""]:
                line = line.strip().replace(".", "")
                if line[0] == "(" and line[-1] == ")":
                    continue
                elif line.isdigit() and len(line) >= 4:
                    new_ids.append(line)
                else:
                    break
    return new_ids


def parse_process_paragraphs(file_path: str, old_ids_n: int) -> List[str]:
    """
    Return empty list if document is invalid.
    """
    process_paragraphs = []
    passed_ids = False
    passed_potential_overlap = False
    p = ""
    temp = ""

    with open(file_path) as f:
        for line in f:
            if not passed_ids:
                if line[0] == "(" or line[0].isdigit() or line in ["\n", "\r\n"]:
                    continue
                else:
                    passed_ids = True
            # passed_ids
            if line in ["\n", "\r\n"]:
                temp = p
                p = ""
            else:
                new_paragraph = False
                if len(line.split()) >= 2:
                    check = line.split()[:2]
                    if (
                        check[0].replace(".", "")
                        in ["Prozeß", "Frozeß", "Ermittlungsverfahren"]
                        and check[1].replace(".", "") == "gegen"
                    ):
                        new_paragraph = True
                        passed_potential_overlap = True
                if new_paragraph and not temp == "":
                    if passed_potential_overlap:
                        process_paragraphs.append(temp)
                        temp = ""
                        p = line
                else:
                    p += temp + line
                    temp = ""
    # TODO check potential non finished process paragraph/ overlap --accumulate all lines of a type?
    if p != "":
        process_paragraphs.append(p)
    elif temp != "":
        process_paragraphs.append(temp)

    for i, s in enumerate(process_paragraphs):
        process_paragraphs[i] = remove_linebreak_hyphen(s)

    return process_paragraphs


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
