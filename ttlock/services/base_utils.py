import json


def write_to_json(content, file_name):
    with open(file_name, 'w') as outfile:
        json.dump(content, outfile,sort_keys=False,indent=4, ensure_ascii=False)


def open_to_json(file_name):
    with open(file_name, 'r') as outfile:
        data = json.load(outfile)
    return data