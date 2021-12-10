import os
import json
import shutil
from pathlib import Path
from typing import List

parsed_documents_n = 0
invalid_document_name_n = 0
invalid_id_paragraph_n = 0
valid_document_n = 0


class Error(Exception):
    '''Base class for other exceptions.'''
    pass


class InvalidDocumentName(Error):
    '''Raised when document name is not valid.'''
    pass


class InvalidIdParagraph(Error):
    '''Raised when document id paragraph is not valid.'''
    pass


class ProcessNumberException(Error):
    '''Raised when process number can't be parsed, related to process documents.'''
    pass


class ProcedureNumberException(Error):
    '''Raised when procedure number can't be parsed, related to proceedings discontinued by the courts.'''
    pass


class PeopleNameException(Error):
    '''Raised when names of persons can't be parsed.'''
    pass


class OccupationException(Error):
    '''Raised when occupation can't be parsed.'''
    pass


class BirthdateException(Error):
    '''Raised when birthdate can't be parsed.'''
    pass


class JudgmentException(Error):
    '''Raised when judgment can't be parsed.'''
    pass


class AttachmentsException(Error):
    '''Raised when attachments can't be parsed.'''
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
    global invalid_id_paragraph_n, valid_document_n
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

        # end of "parser" -> no expection raised
        valid_document_n += 1

    except InvalidIdParagraph:
        source = file_path
        dest = os.path.join(
            cwd, "output/invalid_documents/id_paragraph/"+file_name)
        shutil.copyfile(source, dest)
        invalid_id_paragraph_n += 1
    return d


def exec():
    global parsed_documents_n, invalid_document_name_n, invalid_id_paragraph_n, valid_document_n
    d = {}
    d["Statistiken"] = {}
    d["Statistiken"]["Allgemein"] = {}
    d["Statistiken"]["Info_Ungültige_Dokumente"] = {}
    d["Dokumente"] = {}

    cwd = os.getcwd()
    path_txt = os.path.join(cwd, "text")
    Path(os.path.join(cwd, "output")).mkdir(parents=True, exist_ok=True)
    path_invalid_docs = os.path.join(cwd, "output/invalid_documents")
    path_invalid_document_name = os.path.join(
        path_invalid_docs, "document_name")
    path_invalid_id_paragraph = os.path.join(
        path_invalid_docs, "id_paragraph")
    try:
        Path(path_invalid_docs).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        # rm /output/invalid_documents and create a new dir
        shutil.rmtree(path_invalid_docs, ignore_errors=True)
        shutil.rmtree(path_invalid_document_name, ignore_errors=True)
        shutil.rmtree(path_invalid_id_paragraph, ignore_errors=True)
        Path(path_invalid_docs).mkdir(parents=True, exist_ok=True)
        Path(path_invalid_document_name).mkdir(parents=True, exist_ok=True)
        Path(path_invalid_id_paragraph).mkdir(parents=True, exist_ok=True)
    process_types = []

    for path, dir, files in os.walk(path_txt):
        process_types = dir
        break

    # [('/home/andreas/dh/text_to_json/text/Eingestellte_Verfahren', 'Eingestellte_Verfahren'), ...]
    process_paths_and_types = []  # (path,type)

    for type in process_types:
        process_paths_and_types.append((os.path.join(path_txt, type), type))
        d["Dokumente"][type] = []

    for (p, t) in process_paths_and_types:
        for path, dir, files in os.walk(p):
            # [('00118', '00118-NSJUSTIZ-BAND3-Teil_1-3_1_a_Prozesse_1934-20190129T163853l__PROCESSED.txt'), ...]
            ids_and_filenames = []  # (id,file)

            for file in files:
                try:
                    id = file[:5]

                    if not (len(id) == 5 and id.isdigit()):
                        raise InvalidDocumentName

                    ids_and_filenames.append((int(id), file))
                except InvalidDocumentName:
                    source = path+"/"+file
                    dest = os.path.join(
                        cwd, "output/invalid_documents/document_name/"+file)
                    shutil.copyfile(source, dest)
                    invalid_document_name_n += 1
                finally:
                    parsed_documents_n += 1
            ids_and_filenames.sort(key=lambda x: x[0])
            d["Dokumente"][t] = {}

            for (id, f) in ids_and_filenames:
                d["Dokumente"][t][id] = text_segmentation_alg(
                    os.path.join(path, f), f)
                # break  # TODO rm debug help
        # break  # TODO rm debug help

    # Add stats
    d["Statistiken"]["Allgemein"]["Gültige_Dokumente_Gesamt"] = valid_document_n
    d["Statistiken"]["Allgemein"]["Ungültige_Dokumente_Gesamt"] = invalid_document_name_n + \
        invalid_id_paragraph_n
    d["Statistiken"]["Allgemein"]["Anzahl_Dokumente_Gesamt"] = d["Statistiken"]["Allgemein"]["Gültige_Dokumente_Gesamt"] + \
        d["Statistiken"]["Allgemein"]["Ungültige_Dokumente_Gesamt"]
    d["Statistiken"]["Allgemein"]["Anzahl_Verarbeitete_Dokumente_Prüfsumme"] = parsed_documents_n
    d["Statistiken"]["Allgemein"]["Anteil_Gültige_Dokumente"] = round(
        d["Statistiken"]["Allgemein"]["Gültige_Dokumente_Gesamt"] / d["Statistiken"]["Allgemein"]["Anzahl_Dokumente_Gesamt"], 4)
    d["Statistiken"]["Allgemein"]["Ungültige_Prozesse_Gesamt"] = "TODO: Identifiziere Anzahl an Prozessabsätzen in ungültigen Dokumenten"
    d["Statistiken"]["Allgemein"]["Gültige_Prozesse_Gesamt"] = "TODO"
    d["Statistiken"]["Allgemein"]["Anteil_Gültige_Prozesse"] = "TODO"

    # Add "invalid documents info"
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Dokument_Name"] = invalid_document_name_n
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Id_Absatz"] = invalid_id_paragraph_n
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Prozessnummer"] = "TODO"
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Verfahrensnummer"] = "TODO"
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Personen_Name"] = "TODO"
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Beruf"] = "TODO"
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Geburtsdatum"] = "TODO"
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Urteil"] = "TODO"
    d["Statistiken"]["Info_Ungültige_Dokumente"]["Anlagen"] = "TODO"

    with open(os.path.join(cwd, 'output/output.json'), mode='w', encoding="utf-8") as fp:
        json.dump(d, fp, ensure_ascii=False)


if __name__ == "__main__":
    exec()
