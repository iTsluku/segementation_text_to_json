import os
import json


def exec():
    '''
    assumptions:
    + first 5 chars, given a text file, define the order within a process type subdir 
    '''
    d = {}
    cwd = os.getcwd()
    path_txt = os.path.join(cwd, "text")

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
                id = file[:5]
                # TODO try catch
                ids_and_filenames.append((int(id), file))
            ids_and_filenames.sort(key=lambda x: x[0])
            d[t] = {}

            for (id, f) in ids_and_filenames:
                d[t][id] = f  # TODO text file segmenattion

    with open(os.path.join(cwd, 'output.json'), 'w') as fp:
        json.dump(d, fp)


if __name__ == "__main__":
    exec()
