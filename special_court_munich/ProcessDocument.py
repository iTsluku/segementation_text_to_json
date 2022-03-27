from typing import List


def get_old_ids(file_path: str) -> List[str]:
    old_ids = []

    with open(file_path) as f:
        for line in f:
            if line not in ["\n", "\r\n", ""]:
                line = line.strip().replace(".", "")
                if line[0] == "(" and line[-1] == ")":
                    line = line.replace("(", "").replace(")", "")
                    if line.isdigit() and len(line) >= 3:
                        old_ids.append(line)
                else:
                    break
    return old_ids


def get_new_ids(file_path: str) -> List[str]:
    new_ids = []

    with open(file_path) as f:
        for line in f:
            if line not in ["\n", "\r\n", ""]:
                line = line.strip().replace(".", "")
                if line[0] == "(" and line[-1] == ")":
                    continue
                elif line.isdigit() and len(line) >= 4:
                    new_ids.append(line)
                else:
                    break
    return new_ids
