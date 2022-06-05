import json
import os
import re
from pathlib import Path

from special_court_munich.corpus import CorpusStats
from special_court_munich.process_document import text_segmentation_alg

pattern_file_with_segments = re.compile(r"^.*\d+_\d{5}.txt$")
pattern_filename_id = re.compile(r"^.*\d+_(\d{5}).txt$")


def main():
    cwd = os.getcwd()
    output_path_abs = os.path.join(cwd, "output/output.json")
    corpus_stats = CorpusStats()
    data = {"stats": {}, "proceedings": []}
    Path(os.path.join(cwd, "output")).mkdir(parents=True, exist_ok=True)
    # change input dir path here
    text_new_dir_path = os.path.join(cwd, "input/text_tesseract_param_6")
    text_directory = os.fsencode(text_new_dir_path)

    ids_and_filenames = []  # (id,file)
    for file in os.listdir(text_directory):
        filename = os.fsdecode(file)
        # filter Register, Info, ...
        match = pattern_file_with_segments.search(filename)
        if not (filename.endswith(".txt") and match):
            continue
        document_id = pattern_filename_id.findall(filename)[0]
        ids_and_filenames.append((int(document_id), filename))
    ids_and_filenames.sort(key=lambda x: x[0])

    for i, (document_id, filename) in enumerate(ids_and_filenames):
        proceedings, corpus_stats = text_segmentation_alg(
            os.path.join(text_new_dir_path, filename),
            filename,
            str(document_id),
            corpus_stats,
        )
        for p in proceedings:
            data["proceedings"].append(p)
    data["stats"] = corpus_stats.get_repr_dict()
    with open(output_path_abs, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
