import string
from typing import List, Tuple

from nltk.tokenize import word_tokenize
from special_court_munich import preprocess_segment, process_segment
from special_court_munich.corpus import CorpusStats

PUNCTUATION = string.punctuation


class InvalidIdParagraph(Exception):
    """Raised when the document id paragraph is not valid, given column search."""

    pass


class ParagraphSegmentationException(Exception):
    """Raised when the paragraphs can't be segmented, given column search."""

    pass


class RowFormatException(Exception):
    """Raised when the text structure doesn't match the row search format."""

    pass


process_paragraph_start_fst_words = [
    "Prozeß",
    "Frozeß",
    "Ermittlungsverfahren",
    "bErmittlungsverfahren",
]
process_paragraph_start_snd_words = ["gegen"]


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


class ColumnFormat:
    @staticmethod
    def get_old_ids(file_path: str) -> List[str]:
        old_ids = []

        with open(file_path) as f:
            found_old_id = False
            for line in f:
                if line not in ["\n", "\r\n", ""]:
                    line = line.strip().replace(".", "")
                    if line and line[0] == "(" and line[-1] == ")":
                        line = line.replace("(", "").replace(")", "")
                        if line and line.isdigit():
                            old_ids.append(line)
                            found_old_id = True
                    elif found_old_id:
                        break
        return old_ids

    @staticmethod
    def get_new_ids(file_path: str) -> List[str]:
        new_ids = []

        with open(file_path) as f:
            found_new_id = False
            for i, line in enumerate(f):
                if line not in ["\n", "\r\n", ""]:
                    line = line.strip().replace(".", "")
                    if line and line[0] == "(" and line[-1] == ")":
                        continue
                    elif line.isdigit() and i > 1:
                        # filter first 2 rows
                        new_ids.append(line)
                        found_new_id = True
                    elif found_new_id:
                        break
        return new_ids

    @staticmethod
    def get_process_paragraphs(file_path: str) -> List[str]:
        """
        Return empty list if document is invalid.
        """
        process_paragraphs = []
        passed_ids = False
        passed_doc_overlap_after_ids = False
        passed_potential_overlap = False
        p = ""
        temp = ""

        with open(file_path) as f:
            for i, line in enumerate(f):
                if not passed_ids:
                    if line[0] == "(" or line[0].isdigit() or line in ["\n", "\r\n"]:
                        continue
                    elif i >= 3:
                        # min 4 rows with id content
                        passed_ids = True
                # passed_ids
                if not passed_doc_overlap_after_ids:
                    if line in ["\n", "\r\n"]:
                        continue
                    check = line.split()[:2]
                    if not (
                        check[0].replace(".", "") in process_paragraph_start_fst_words
                        and check[1].replace(".", "")
                        in process_paragraph_start_snd_words
                    ):
                        continue
                    else:
                        passed_doc_overlap_after_ids = True
                        temp = p
                        p = ""

                if line in ["\n", "\r\n"]:
                    temp = p
                    p = ""
                else:
                    new_paragraph = False
                    if len(line.split()) >= 2:
                        check = line.split()[:2]
                        if (
                            check[0].replace(".", "")
                            in process_paragraph_start_fst_words
                            and check[1].replace(".", "")
                            in process_paragraph_start_snd_words
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
        if p != "":
            process_paragraphs.append(p)
        elif temp != "":
            process_paragraphs.append(temp)

        for i, s in enumerate(process_paragraphs):
            process_paragraphs[i] = remove_linebreak_hyphen(s)
        return process_paragraphs

    @staticmethod
    def parse_document(
        file_path: str, filename: str, document_id: str, corpus_stats: CorpusStats
    ):
        """
        Return list with processes, empty list if document is invalid.
        """
        process_paragraphs_dict_list = []
        old_ids = ColumnFormat.get_old_ids(file_path)
        new_ids = ColumnFormat.get_new_ids(file_path)

        if len(old_ids) == 0 or len(new_ids) == 0 or len(old_ids) != len(new_ids):
            raise InvalidIdParagraph

        process_paragraphs = ColumnFormat.get_process_paragraphs(file_path)
        process_paragraphs = preprocess_segment.preprocess_processes(process_paragraphs)

        if len(process_paragraphs) != len(old_ids):
            raise ParagraphSegmentationException

        for i, process_paragraph in enumerate(process_paragraphs):
            paragraph_as_dict, corpus_stats = process_segment.parse_process_segment(
                filename,
                old_ids[i],
                new_ids[i],
                document_id,
                process_paragraph,
                corpus_stats,
            )
            # check if dict is empty --exception was raised while parsing segments for the given paragraph
            if paragraph_as_dict:
                process_paragraphs_dict_list.append(paragraph_as_dict)
        return process_paragraphs_dict_list, corpus_stats


class RowFormat:
    @staticmethod
    def is_new_process_segment(words: List[str]) -> bool:
        if len(words) < 4:
            return False
        if not words[0].isdigit():
            return False
        if not words[1].isdigit():
            return False
        if words[2] not in process_paragraph_start_fst_words:
            return False
        if words[3] not in process_paragraph_start_snd_words:
            return False
        return True

    @staticmethod
    def get_process_text_after_indices(text: str) -> str:
        o = ""
        k = 0
        for c in text:
            if k == 4:
                o += c
            elif k == 0 and c.isdigit():
                k = 1
            elif k == 1 and not c.isdigit():
                k = 2
            elif k == 2 and c.isdigit():
                k = 3
            elif k == 3 and not c.isdigit():
                k = 4
        return o.lstrip()

    @staticmethod
    def parse_document(
        file_path: str, filename: str, document_id: str, corpus_stats: CorpusStats
    ):
        process_paragraphs_dict_list = []
        old_ids = []
        new_ids = []
        process_paragraphs = []
        temp = ""
        with open(file_path) as f:
            for i, line in enumerate(f):
                # remove punctuation for new process segment check
                line_mod = ""
                for c in line:
                    if c not in PUNCTUATION:
                        line_mod += c
                line_mod = line_mod.strip()
                words = word_tokenize(line_mod, language="german")
                if RowFormat.is_new_process_segment(words):
                    if temp != "":
                        process_paragraphs.append(temp)
                    old_ids.append(words[0])
                    new_ids.append(words[1])
                    temp = RowFormat.get_process_text_after_indices(line)
                elif temp != "":
                    # TODO optimize
                    # (ocr fail ->) prevent: process paragraph overlap
                    for w1 in process_paragraph_start_fst_words:
                        for w2 in process_paragraph_start_snd_words:
                            w_check = w1 + " " + w2
                            if w_check in line:
                                temp = ""
                    if temp != "":
                        temp += line
                    else:
                        # process paragraph temp reset -> rm ids too
                        old_ids.pop()
                        new_ids.pop()
                        # TODO update corpusstats about pot. missing two proceedings.

        if temp != "":
            process_paragraphs.append(temp)
        if (
            not old_ids
            or not new_ids
            or not process_paragraphs
            or len(old_ids) != len(process_paragraphs)
        ):
            raise RowFormatException
        # TODO mv to segment, because segment needs access to original text
        for i, s in enumerate(process_paragraphs):
            process_paragraphs[i] = remove_linebreak_hyphen(s)
        process_paragraphs = preprocess_segment.preprocess_processes(process_paragraphs)
        for i, process_paragraph in enumerate(process_paragraphs):
            paragraph_as_dict, corpus_stats = process_segment.parse_process_segment(
                filename,
                old_ids[i],
                new_ids[i],
                document_id,
                process_paragraph,
                corpus_stats,
            )
            # check if dict is empty --exception was raised while parsing segments for the given paragraph
            if paragraph_as_dict:
                process_paragraphs_dict_list.append(paragraph_as_dict)

        return process_paragraphs_dict_list, corpus_stats


def text_segmentation_alg(
    file_path: str, filename: str, document_id: str, corpus_stats: CorpusStats
) -> Tuple[List[dict], CorpusStats]:
    process_paragraphs_dict_list = []
    try:
        # try column format
        process_paragraphs_dict_list, corpus_stats = ColumnFormat.parse_document(
            file_path, filename, document_id, corpus_stats
        )
        corpus_stats.inc_val_valid_docs()
    except (InvalidIdParagraph, ParagraphSegmentationException):
        # colum format failed -> try row format
        try:
            process_paragraphs_dict_list, corpus_stats = RowFormat.parse_document(
                file_path, filename, document_id, corpus_stats
            )
            corpus_stats.inc_val_valid_docs()
        except RowFormatException:
            # print("failed:", file_path)
            pass
    finally:
        corpus_stats.inc_val_parsed_docs()
        return process_paragraphs_dict_list, corpus_stats
