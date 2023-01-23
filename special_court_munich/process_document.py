import string
import bs4
import numpy as np
from typing import List, Tuple, Optional, Union
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


class HOCRFormat:
    @staticmethod
    def get_regest_text_x1_estimate(paragraphs):
        x1s = []
        for paragraph in paragraphs:
            lines = paragraph.find_all("span", class_="ocr_line")
            for line in lines:
                words = line.find_all("span", class_="ocrx_word")
                if not words:
                    continue
                x1 = int(words[0]["title"].split()[1])
                x1s.append(x1)
        return np.median(x1s)  # median :: ignore outliers, assume enough lines

    @staticmethod
    def is_paragraph_new_regest(
        paragraph: bs4.element.Tag, regest_text_x1_estimate, document_id
    ) -> bool:
        lines = paragraph.find_all("span", class_="ocr_line")
        if not lines:
            return False
        line_check = lines[0]
        words = line_check.find_all("span", class_="ocrx_word")
        if not words:
            return False
        # check index x1 < 1400
        check = words[0].text
        if check.startswith(document_id):
            return False
        offset = abs(int(words[0]["title"].split()[1]) - regest_text_x1_estimate)
        if (
            800 < offset < 1200
            and check not in string.punctuation  # no punctuation
            and any(i.isdigit() for i in check)  # min one digit
        ):
            return True
        return False

    @staticmethod
    def is_line_new_regest(
        line: bs4.element.Tag, regest_text_x1_estimate, document_id
    ) -> bool:
        words = line.find_all("span", class_="ocrx_word")
        if not words:
            return False
        check = words[0].text
        if check.startswith(document_id):
            return False
        offset = abs(int(words[0]["title"].split()[1]) - regest_text_x1_estimate)
        if (
            800 < offset < 1200
            and check not in string.punctuation  # no punctuation --TODO rm?
            and any(i.isdigit() for i in check)  # min one digit --TODO rm?
        ):
            return True
        return False

    @staticmethod
    def get_index(paragraph: bs4.element.Tag) -> Optional[str]:
        lines = paragraph.find_all("span", class_="ocr_line")

        if not lines:
            return None
        line_check = lines[0]
        words = line_check.find_all("span", class_="ocrx_word")

        if not words:
            return None
        check = words[0].text

        if check[0] == "(" and check[-1] == ")" and check[1:-1].isdigit():
            return check.replace("(", "").replace(")", "").strip()
        return None

    @staticmethod
    def get_index_by_line(line: bs4.element.Tag) -> Optional[str]:
        words = line.find_all("span", class_="ocrx_word")

        if not words:
            return None
        check = words[0].text

        if check[0] == "(" and check[-1] == ")" and check[1:-1].isdigit():
            return check.replace("(", "").replace(")", "").strip()
        return None

    @staticmethod
    def get_shelfmark(paragraph: bs4.element.Tag) -> Optional[str]:
        lines = paragraph.find_all("span", class_="ocr_line")

        if not lines:
            return None
        line_check = lines[0]
        words = line_check.find_all("span", class_="ocrx_word")

        if not words or len(words) < 2:
            return None
        check = words[1].text

        if check.isdigit():
            return check
        return None

    @staticmethod
    def get_shelfmark_by_line(
        line: bs4.element.Tag, second_line: Union[bs4.element.Tag, None]
    ) -> Optional[str]:
        words = line.find_all("span", class_="ocrx_word")

        if not words or len(words) < 2:
            return None
        check = words[1].text.strip()
        if check == "in:":
            if second_line:
                words_snd = second_line.find_all("span", class_="ocrx_word")
                check = words_snd[0].text.strip()
        if check.isdigit():
            return check
        return None

    @staticmethod
    def get_original_regest_text(paragraphs: List[bs4.element.Tag]) -> str:
        # (2) 1352 Prozeß gegen die Hilfsarbeitersehefrau Maria SCHRAUFSTETTER (geb, 27. Aug. 1886) aus Mün- chen
        # wegen unerlaubten Verteilens von kommu- nistischen Flugblättern., Urteil: Freispruch nach Untersuchungshaft
        # Anlage: 2 hektographierte Flugblätter der "Rot Front" 21. Mrz. 1933 - 16, Mai 1933 (S Pr 2/33)
        original_regest_text = []
        for paragraph in paragraphs:
            lines = paragraph.find_all("span", class_="ocr_line")
            for line in lines:
                words = line.find_all("span", class_="ocrx_word")
                for word in words:
                    word = word.text
                    original_regest_text.append(word)
        return " ".join(original_regest_text)

    @staticmethod
    def get_original_regest_text_by_lines(lines: List[bs4.element.Tag]) -> str:
        original_regest_text = []
        for line in lines:
            words = line.find_all("span", class_="ocrx_word")
            for word in words:
                word = word.text
                original_regest_text.append(word)
        return " ".join(original_regest_text)

    @staticmethod
    def get_preprocessed_regest_text(paragraphs: List[bs4.element.Tag]) -> str:
        # Prozeß gegen die Hilfsarbeitersehefrau Maria SCHRAUFSTETTER (geb, 27. Aug. 1886) aus München
        # wegen unerlaubten Verteilens von kommunistischen Flugblättern., Urteil: Freispruch nach Untersuchungshaft
        # Anlage: 2 hektographierte Flugblätter der "Rot Front" 21. Mrz. 1933 - 16, Mai 1933 (S Pr 2/33)

        # line break Mün- chen -> München, kommu- nistischen -> kommunistischen
        original_regest_text = []
        for paragraph in paragraphs:
            lines = paragraph.find_all("span", class_="ocr_line")
            for line in lines:
                words = line.find_all("span", class_="ocrx_word")
                for word in words:
                    word = word.text
                    if word == "|":
                        continue
                    if original_regest_text and original_regest_text[-1][-1] == "-":
                        original_regest_text[-1] = (
                            original_regest_text[-1].replace("-", "") + word
                        )
                    else:
                        original_regest_text.append(word)
        return " ".join(original_regest_text[2:])

    @staticmethod
    def get_preprocessed_regest_text_by_lines(lines: List[bs4.element.Tag]) -> str:
        original_regest_text = []
        for line in lines:
            words = line.find_all("span", class_="ocrx_word")
            for word in words:
                word = word.text
                if word == "|":
                    continue
                if original_regest_text and original_regest_text[-1][-1] == "-":
                    original_regest_text[-1] = (
                        original_regest_text[-1].replace("-", "") + word
                    )
                else:
                    original_regest_text.append(word)
        return " ".join(original_regest_text[2:])

    @staticmethod
    def remove_page_number_forward_pass(
        lines: List[bs4.element.Tag],
    ) -> List[bs4.element.Tag]:
        if not lines:
            return lines
        words_last_line = lines[-1].find_all("span", class_="ocrx_word")
        if not words_last_line or len(words_last_line) > 1:
            return lines
        if words_last_line[0].getText().strip().isdigit():
            # if line equals page number line, then remove
            return lines[:-1]
        return lines

    @staticmethod
    def parse_document(
        file_path: str,
        filename: str,
        document_id: str,
        corpus_stats: CorpusStats,
        forward_pass: [bs4.element.Tag],
    ):
        process_paragraphs_dict_list = []
        temp_lines = HOCRFormat.remove_page_number_forward_pass(forward_pass)

        with open(file_path, "r") as file:
            soup = bs4.BeautifulSoup(file, "html.parser")
            _check = soup.find_all("div", class_="ocr_carea")
            if not _check:
                # TODO check
                return process_paragraphs_dict_list, corpus_stats, temp_lines

            x_min, y_min, x_max, y_max = _check[0]["title"].split()[1:]
            paragraphs = soup.find_all("p")

            if not paragraphs:
                # TODO check
                return process_paragraphs_dict_list, corpus_stats, temp_lines
            regest_text_x1_estimate = HOCRFormat.get_regest_text_x1_estimate(paragraphs)
            lines = []
            for paragraph in paragraphs:
                lines_ = paragraph.find_all("span", class_="ocr_line")
                lines += lines_
            for line in lines:
                if HOCRFormat.is_line_new_regest(
                    line, regest_text_x1_estimate, document_id
                ):
                    if temp_lines:
                        # process temp lines
                        index = HOCRFormat.get_index_by_line(temp_lines[0])
                        second_line = None
                        if len(temp_lines) >= 2:
                            second_line = temp_lines[1]
                        shelfmark = HOCRFormat.get_shelfmark_by_line(
                            temp_lines[0], second_line
                        )
                        original_regest_text = (
                            HOCRFormat.get_original_regest_text_by_lines(temp_lines)
                        )
                        preprocessed_regest_text = (
                            HOCRFormat.get_preprocessed_regest_text_by_lines(temp_lines)
                        )
                        (
                            paragraph_as_dict,
                            corpus_stats,
                        ) = process_segment.parse_process_segment(
                            filename,
                            index,
                            shelfmark,
                            document_id,
                            preprocessed_regest_text,
                            corpus_stats,
                            process_text_original=original_regest_text,
                        )
                        # check if dict is empty --exception was raised while parsing segments for the given paragraph
                        if paragraph_as_dict:
                            process_paragraphs_dict_list.append(paragraph_as_dict)
                    temp_lines = [line]
                else:
                    if temp_lines:
                        temp_lines.append(line)
        return process_paragraphs_dict_list, corpus_stats, temp_lines


def text_segmentation_alg(
    file_path: str,
    filename: str,
    document_id: str,
    corpus_stats: CorpusStats,
    forward_pass: [bs4.element.Tag],
) -> Tuple[List[dict], CorpusStats, List[bs4.element.Tag]]:
    process_paragraphs_dict_list = []
    (
        process_paragraphs_dict_list,
        corpus_stats,
        forward_pass,
    ) = HOCRFormat.parse_document(
        file_path, filename, document_id, corpus_stats, forward_pass
    )
    if process_paragraphs_dict_list:
        corpus_stats.inc_val_valid_docs()
    # else:
    #    print("file failed:", filename)
    corpus_stats.inc_val_parsed_docs()
    return process_paragraphs_dict_list, corpus_stats, forward_pass
