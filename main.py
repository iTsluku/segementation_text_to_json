import os
import json
import shutil
from pathlib import Path


class Error(Exception):
    '''Base class for other exceptions'''
    pass


class InvalidDocumentName(Error):
    '''Raised when document name is not valid'''
    pass


def text_segmentation_alg(f: str) -> dict:
    d = {
        "file_name": f,
        "Prozessnummer": "???",
        "Verfahrensnummer": "???",
        "Name": "???",
        "Beruf": "???",
        "Geburtsdatum": "???",
        "Urteil": "???",
        "Anlagen": "???",
    }
    return d


def exec():
    d = {}
    cwd = os.getcwd()
    path_txt = os.path.join(cwd, "text")
    Path(os.path.join(cwd, "output")).mkdir(parents=True, exist_ok=True)
    path_invalid_docs = os.path.join(cwd, "output/invalid_documents")
    try:
        Path(path_invalid_docs).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        # rm /output/invalid_documents and create a new dir
        shutil.rmtree(path_invalid_docs, ignore_errors=True)
        Path(path_invalid_docs).mkdir(parents=True, exist_ok=True)
    process_types = []

    for path, dir, files in os.walk(path_txt):
        process_types = dir
        break

    # [('/home/andreas/dh/text_to_json/text/Eingestellte_Verfahren', 'Eingestellte_Verfahren'), ...]
    process_paths_and_types = []  # (path,type)

    for type in process_types:
        process_paths_and_types.append((os.path.join(path_txt, type), type))
        d[type] = []

    for (p, t) in process_paths_and_types:
        for path, dir, files in os.walk(p):
            # [('00118', '00118-NSJUSTIZ-BAND3-Teil_1-3_1_a_Prozesse_1934-20190129T163853l__PROCESSED.txt'), ...]
            ids_and_filenames = []  # (id,file)

            for file in files:
                try:
                    id = file[:5]

                    if not (len(id) == 5 and id.isdigit()):
                        raise InvalidDocumentName
                    else:
                        ids_and_filenames.append((int(id), file))
                except InvalidDocumentName:
                    source = path+"/"+file
                    dest = os.path.join(cwd, "output/invalid_documents/"+file)
                    shutil.copyfile(source, dest)
            ids_and_filenames.sort(key=lambda x: x[0])
            d[t] = {}

            for (id, f) in ids_and_filenames:
                d[t][id] = text_segmentation_alg(f)

    with open(os.path.join(cwd, 'output/output.json'), 'w') as fp:
        json.dump(d, fp)


if __name__ == "__main__":
    exec()
