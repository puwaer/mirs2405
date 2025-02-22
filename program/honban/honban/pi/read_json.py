import json

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def read_json_name(file_number):
    file_path = [
        '/home/pi/Documents/mirs2405/honban/pc_data/output_head_depth.json',
        '/home/pi/Documents/mirs2405/honban/pc_data/output_foot_depth.json',
        '/home/pi/Documents/mirs2405/honban/pc_data/output_zed.json',
        ]
    
    return int(read_json(file_path[file_number]))
    

if __name__ == "__main__":
    json_data = read_json_name(2)       #[0, 1, 2],[男女, 年齢, 身長]
                                        # 0: 男性, 1: 女性
    print(json_data)
    