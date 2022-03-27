import os
import json

from pathlib import Path
from typing import List

from special_court_munich import PreprocessSegment
from special_court_munich import ProcessSegment
from special_court_munich import ProcessDocument
from special_court_munich.CorpusStats import CorpusStats


class InvalidDocumentName(Exception):
    """Raised when the document name is not valid."""

    pass


class InvalidIdParagraph(Exception):
    """Raised when the document id paragraph is not valid."""

    pass


class ParagraphSegmentationException(Exception):
    """Raised when the paragraphs can't be segmented."""

    pass


# setup
cwd = os.getcwd()
corpus_stats = CorpusStats()


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
        process_paragraphs[i] = PreprocessSegment.remove_linebreak_hyphen(s)

    return process_paragraphs


def text_segmentation_alg(file_path: str, document_id: str) -> List[dict]:
    global corpus_stats
    """
    Return list with processes, empty list if document is invalid.
    """
    process_paragraphs_dict_list = []
    try:
        old_ids = ProcessDocument.get_old_ids(file_path)
        new_ids = ProcessDocument.get_new_ids(file_path)

        if len(old_ids) == 0 or len(new_ids) == 0 or len(old_ids) != len(new_ids):
            raise InvalidIdParagraph

        process_paragraphs = parse_process_paragraphs(file_path, len(old_ids))
        process_paragraphs = PreprocessSegment.preprocess_processes(process_paragraphs)

        if len(process_paragraphs) != len(old_ids):
            raise ParagraphSegmentationException

        for i, process_paragraph in enumerate(process_paragraphs):
            paragraph_as_dict, corpus_stats = ProcessSegment.parse_process_segment(
                old_ids[i], new_ids[i], document_id, process_paragraph
            )
            # check if dict is empty --exception was raised while parsing segments for the given paragraph
            if paragraph_as_dict:
                process_paragraphs_dict_list.append(paragraph_as_dict)

        # end of "parser" -> no exception raised
        corpus_stats.inc_val_valid_docs()
    except InvalidIdParagraph:
        pass
    except ParagraphSegmentationException:
        pass
    finally:
        corpus_stats.inc_val_parsed_docs()
        return process_paragraphs_dict_list


def main():
    dictionary = {"CorpusStats": {}, "Dokumente": {}}
    path_txt = os.path.join(cwd, "text")
    Path(os.path.join(cwd, "output")).mkdir(parents=True, exist_ok=True)
    process_types = []

    for path, dir, files in os.walk(path_txt):
        process_types = dir
        break

    # [('/home/andreas/dh/text_to_json/text/Eingestellte_Verfahren', 'Eingestellte_Verfahren'), ...]
    process_paths_and_types = []  # (path,process_type)

    for process_type in process_types:
        process_paths_and_types.append(
            (os.path.join(path_txt, process_type), process_type)
        )
        dictionary["Dokumente"][process_type] = []

    for (p, t) in process_paths_and_types:
        for path, _, files in os.walk(p):
            # [('00118', '00118-NSJUSTIZ-BAND3-Teil_1-3_1_a_Prozesse_1934-20190129T163853l__PROCESSED.txt'), ...]
            ids_and_filenames = []  # (id,file)

            for file in files:
                try:
                    document_id = file[:5]

                    if not (len(document_id) == 5 and document_id.isdigit()):
                        raise InvalidDocumentName

                    ids_and_filenames.append((int(document_id), file))
                except InvalidDocumentName:
                    pass
            ids_and_filenames.sort(key=lambda x: x[0])
            dictionary["Dokumente"][t] = []

            for (document_id, f) in ids_and_filenames:
                p_d_list = text_segmentation_alg(
                    os.path.join(path, f), str(document_id)
                )
                for p_d in p_d_list:
                    dictionary["Dokumente"][t].append(p_d)
    dictionary["CorpusStats"] = corpus_stats.get_repr_dict()
    with open(
        os.path.join(cwd, "output/output.json"), mode="w", encoding="utf-8"
    ) as fp:
        json.dump(dictionary, fp, ensure_ascii=False)


if __name__ == "__main__":
    main()
