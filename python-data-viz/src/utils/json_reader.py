def read_json(file_path):
    import json

    with open(file_path, 'r') as file:
        data = json.load(file)

    return data