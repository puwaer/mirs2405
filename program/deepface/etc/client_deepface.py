import socket
import json
import re

def get_dict_data(sock):
    data = sock.recv(1024).decode('utf-8')
    clean_data = re.sub(r'[^\d]', '', data)
    return clean_data

def get_data(HOST, PORT, output_file_1, output_file_2):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            received_data = get_dict_data(sock)
            if received_data:
                # Split number into first digit and remaining digits
                first_digit = int(received_data[0])
                remaining_digits = int(received_data[1:]) if len(received_data) > 1 else 0
                
                # Save first digit to output_file_1
                with open(output_file_1, 'w') as f1:
                    json.dump(first_digit, f1)
                
                # Save remaining digits to output_file_2
                with open(output_file_2, 'w') as f2:
                    json.dump(remaining_digits, f2)
                
                print(f"First digit: {first_digit}, Remaining: {remaining_digits}")

            sock.close()
            
        except KeyboardInterrupt:
            print("\nClosing connection...")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            sock.close()
            continue

if __name__ == "__main__":
    HOST = '172.25.14.19'
    PORT = 5000
    output_file_1 = './program/output/output_age.json'
    output_file_2 = './program/output/output_gender.json'
    get_data(HOST, PORT, output_file_1, output_file_2)