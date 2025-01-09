import json

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    file_path = 'output_zed.json'
    json_data = read_json(file_path)
    #json_data = int(read_json(file_path))
    print(json_data)