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
    process_paths_types = []  # (path,type)

    for type in process_types:
        process_paths_types.append((os.path.join(path_txt, type), type))
        d[type] = []

    for (p, t) in process_paths_types:
        for path, dir, files in os.walk(p):
            # [('00118', '00118-NSJUSTIZ-BAND3-Teil_1-3_1_a_Prozesse_1934-20190129T163853l__PROCESSED.txt'), ...]
            txt_id = []  # (id,file)
            for file in files:
                id = file[:5]
                # TODO try catch
                txt_id.append((int(id), file))
            txt_id.sort(key=lambda x: x[0])
            d[t] = [x[1] for x in txt_id]

    with open(os.path.join(cwd, 'output.json'), 'w') as fp:
        json.dump(d, fp)


if __name__ == "__main__":
    exec()
