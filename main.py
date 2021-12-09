import os
import json
import shutil
from pathlib import Path
from typing import List

invalid_document_name_n = 0
invalid_id_paragraph_n = 0


class Error(Exception):
    '''Base class for other exceptions'''
    pass


class InvalidDocumentName(Error):
    '''Raised when document name is not valid'''
    pass


class InvalidIdParagraph(Error):
    '''Raised when document id paragraph is not valid'''
    pass


def get_old_ids(file_path: str) -> List[str]:
    old_ids = []

    with open(file_path) as f:
        for line in f:
            if line not in ['\n', '\r\n', '']:
                line = line.strip()
                if line[0] == '(' and line[-1] == ')':
                    line = line.replace('(', '').replace(')', '')
                    if line.isdigit():
                        old_ids.append(line)
                else:
                    break
    return old_ids


def get_new_ids(file_path: str) -> List[str]:
    new_ids = []

    with open(file_path) as f:
        for line in f:
            if line not in ['\n', '\r\n', '']:
                line = line.strip()
                if line[0] == '(' and line[-1] == ')':
                    continue
                elif line.isdigit():
                    new_ids.append(line)
                else:
                    break
    return new_ids


def parse_process_paragraphs(file_path: str, n: int) -> List[List[str]]:
    '''
    Return empty list if document is invalid.
    '''
    process_paragraphs = []
    passed_ids = False

    with open(file_path) as f:
        for line in f:
            if not passed_ids:
                pass
            pass  # TODO
    return process_paragraphs


def text_segmentation_alg(file_path: str, file_name: str) -> dict:
    global invalid_id_paragraph_n
    '''
    Store invalid documents.
    Return empty dictionary if document is invalid.
    '''
    try:
        cwd = os.getcwd()
        d = {}
        old_ids = get_old_ids(file_path)
        new_ids = get_new_ids(file_path)

        if len(old_ids) != len(new_ids):
            raise InvalidIdParagraph

        process_paragraphs = parse_process_paragraphs(file_path, len(old_ids))

        for i in range(len(old_ids)):
            d[f'{old_ids[i]} {new_ids[i]}'] = {}

    except InvalidIdParagraph:
        source = file_path
        dest = os.path.join(cwd, "output/invalid_documents/"+file_name)
        shutil.copyfile(source, dest)
        invalid_id_paragraph_n += 1
    '''
    d = {
        "Prozessnummer": "???",
        "Verfahrensnummer": "???",
        "Name": "???",
        "Beruf": "???",
        "Geburtsdatum": "???",
        "Urteil": "???",
        "Anlagen": "???",
    }
    '''
    return d


def exec():
    global invalid_document_name_n, invalid_id_paragraph_n
    d = {}
    d["Info_Ungültige_Dokumente"] = {}
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
                    invalid_document_name_n += 1
            ids_and_filenames.sort(key=lambda x: x[0])
            d[t] = {}

            for (id, f) in ids_and_filenames:
                d[t][id] = text_segmentation_alg(os.path.join(path, f), f)
                # break  # TODO rm debug help
        # break  # TODO rm debug help

    # Add invalid documents info
    d["Info_Ungültige_Dokumente"]["Dokument_Name"] = invalid_document_name_n
    d["Info_Ungültige_Dokumente"]["Id_Absatz"] = invalid_id_paragraph_n

    with open(os.path.join(cwd, 'output/output.json'), mode='w', encoding="utf-8") as fp:
        json.dump(d, fp, ensure_ascii=False)


if __name__ == "__main__":
    exec()
