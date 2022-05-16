import os
import json

from pathlib import Path
from special_court_munich.corpus import CorpusStats
from special_court_munich.process_document import text_segmentation_alg


class InvalidDocumentName(Exception):
    """Raised when the document name is not valid."""

    pass


def main():
    cwd = os.getcwd()
    output_path_abs = os.path.join(cwd, "output/output.json")
    corpus_stats = CorpusStats()
    data = {"CorpusStats": {}, "Dokumente": {}}
    path_txt = os.path.join(cwd, "text_old")
    Path(os.path.join(cwd, "output")).mkdir(parents=True, exist_ok=True)
    process_types = []

    for path, _dir, files in os.walk(path_txt):
        process_types = _dir
        break

    process_paths_and_types = []  # (path,process_type)

    for process_type in process_types:
        process_paths_and_types.append(
            (os.path.join(path_txt, process_type), process_type)
        )
        data["Dokumente"][process_type] = []

    for (p, t) in process_paths_and_types:
        for path, _, files in os.walk(p):
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
            data["Dokumente"][t] = []

            for (document_id, f) in ids_and_filenames:
                p_d_list, corpus_stats = text_segmentation_alg(
                    os.path.join(path, f), str(document_id), corpus_stats
                )
                for p_d in p_d_list:
                    data["Dokumente"][t].append(p_d)
    data["CorpusStats"] = corpus_stats.get_repr_dict()
    with open(output_path_abs, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
