from typing import List, Tuple

from special_court_munich import preprocess_segment, process_segment
from special_court_munich.corpus import CorpusStats


class InvalidIdParagraph(Exception):
    """Raised when the document id paragraph is not valid."""

    pass


class ParagraphSegmentationException(Exception):
    """Raised when the paragraphs can't be segmented."""

    pass


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


def text_segmentation_alg(
    file_path: str, document_id: str, corpus_stats: CorpusStats
) -> Tuple[List[dict], CorpusStats]:
    """
    Return list with processes, empty list if document is invalid.
    """
    process_paragraphs_dict_list = []
    try:
        old_ids = get_old_ids(file_path)
        new_ids = get_new_ids(file_path)

        if len(old_ids) == 0 or len(new_ids) == 0 or len(old_ids) != len(new_ids):
            raise InvalidIdParagraph

        process_paragraphs = parse_process_paragraphs(file_path, len(old_ids))
        process_paragraphs = preprocess_segment.preprocess_processes(process_paragraphs)

        if len(process_paragraphs) != len(old_ids):
            raise ParagraphSegmentationException

        for i, process_paragraph in enumerate(process_paragraphs):
            paragraph_as_dict, corpus_stats = process_segment.parse_process_segment(
                old_ids[i], new_ids[i], document_id, process_paragraph, corpus_stats
            )
            # check if dict is empty --exception was raised while parsing segments for the given paragraph
            if paragraph_as_dict:
                process_paragraphs_dict_list.append(paragraph_as_dict)
        corpus_stats.inc_val_valid_docs()
    except InvalidIdParagraph:
        pass
    except ParagraphSegmentationException:
        pass
    finally:
        corpus_stats.inc_val_parsed_docs()
        return process_paragraphs_dict_list, corpus_stats
