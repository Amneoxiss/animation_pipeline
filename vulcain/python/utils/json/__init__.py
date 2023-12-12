import json

def load_data(json_file_path):
    with open(json_file_path, "r") as read_file:
        data = json.load(read_file)
    
    return data

def dump_data(json_file_path, data):
    with open(json_file_path, "w") as write_file:
        json.dump(data, write_file)