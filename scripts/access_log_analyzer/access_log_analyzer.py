#!/usr/bin/env python3

import os, sys, re, json

def input_file():
    # Log File Input Control
    file_type = input("Choose log type.\n1. Apache Access Combine\n2. Apache Access Common\n3. Loggly Events JSON\n4. NGINX Access\nEnter q to quit.\n")
    os.system('clear')
    if file_type in ["Q", "q"]:
        sys.exit(1)
    while file_type not in ["1", "2", "3", "4"]:
        file_type = input("Invalid Choice! Enter again or q to quit:")
    os.system('clear')
    #Log Path Input Control
    file_path = input("Enter your file path. Enter q to quit: ")
    os.system('clear')
    if file_path in ["Q", "q"]:
        sys.exit(1)
    while (not os.path.exists(file_path)):
        file_path = input("File not found! Check again and re-enter. Enter q to quit: ")
    os.system('clear')
    return file_type, file_path

def extract_data_from_file(file_type, file_path):
    data = []
    with open(file_path, 'r') as file:
        if file_type in ["1", "4"]:
            for line in file:
                if line.strip():
                    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) [- ]+ \[(\d{2}/\w{3}/\d{4}):(\d{2}:\d{2}:\d{2}) ?\] "(PUT|PUSH|POST|DELETE|GET) (\S+) ((?:HTTP|HTTPS)/\d+\.\d+)" (\d{3}) (\d+) "(.+)" "(.+)"'
                    result = re.match(pattern, line.strip())
                    ip = result.group(1)
                    date = result.group(2)
                    time = result.group(3)
                    method = result.group(4)
                    path = result.group(5)
                    protocol_version = result.group(6)
                    status = int(result.group(7))
                    size = int(result.group(8))
                    referer = result.group(9)
                    user_agent = result.group(10)
                    data.append({"ip":ip, "timestamp":date + ":" + time, "method":method, "path":path, "protocol":protocol_version, "status":status, "size":size, "referer":referer, "user_agent": user_agent})
            return data
        elif file_type == "2":
            for line in file:
                if line.strip():
                    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) [- ]+ \[(\d{2}/\w{3}/\d{4}):(\d{2}:\d{2}:\d{2}) ?\] "(PUT|PUSH|POST|DELETE|GET) (\S+) ((?:HTTP|HTTPS)/\d+\.\d+)" (\d{3}) (\d+)'
                    result = re.match(pattern, line.strip())
                    ip = result.group(1)
                    date = result.group(2)
                    time = result.group(3)
                    method = result.group(4)
                    path = result.group(5)
                    protocol_version = result.group(6)
                    status = int(result.group(7))
                    size = int(result.group(8))
                    data.append({"ip":ip, "timestamp":date + ":" + time, "method":method, "path":path, "protocol":protocol_version, "status":status, "size":size})
            return data
        else:
            for line in file:
                if line.strip():
                    data.append(json.loads(line.strip()))
            return data

def total_number_of_requests(all_data_dict_list):
    return len(all_data_dict_list)

def IP_frequencies(all_data_dict_list):
    IP_frequencies_list = []
    for data in all_data_dict_list:
        updated_ip_list = list(ip["ip"] for ip in IP_frequencies_list)
        if not data["ip"] in updated_ip_list:
            IP_frequencies_list.append({"ip": data["ip"], "requests": 1})
        else:
            IP_index = IP_frequencies_list.index(next(ip for ip in IP_frequencies_list if ip["ip"] == data["ip"]))
            IP_frequencies_list[IP_index]["requests"] += 1
    return sorted(IP_frequencies_list, key = lambda x: x["requests"], reverse=True)

def status_code_destribution(all_data_dict_list):
    status_code_destribution_list = []
    brief_status_list = [{"2xx Success": 0}, {"3xx Redirect": 0}, {"4xx Client Error": 0}, {"5xx Server Error": 0}]
    ###
    for data in all_data_dict_list:
        updated_status_list = list(status["status"] for status in status_code_destribution_list)
        if not data["status"] in updated_status_list:
            status_code_destribution_list.append({"status": data["status"], "frequency": 1})
        else:
            IP_index = status_code_destribution_list.index(next(status for status in status_code_destribution_list if status["status"] == data["status"]))
            status_code_destribution_list[IP_index]["frequency"] += 1
    ###
    for status in status_code_destribution_list:
        if str(status["status"]).startswith("2"):
            brief_status_list[0]["2xx Success"] += status["frequency"]
        elif str(status["status"]).startswith("3"):
            brief_status_list[1]["3xx Redirect"] += status["frequency"]
        elif str(status["status"]).startswith("4"):
            brief_status_list[2]["4xx Client Error"] += status["frequency"]
        elif str(status["status"]).startswith("5"):
            brief_status_list[3]["5xx Server Error"] += status["frequency"]
    ###
    return sorted(status_code_destribution_list, key=lambda x: x["status"]), brief_status_list

def error_percentage(brief_status_list):
    error_count = 0
    total_status = sum(list(frequency.values())[0] for frequency in brief_status_list)
    for status in brief_status_list[2:]:
        error_count += list(status.values())[0]
    return f"{(error_count/total_status)*100:.2f}%"

def hourly_traffics(all_data_dict_list):
    traffics_list = []
    for data in all_data_dict_list:
        ###
        extract_hour = re.match(r".*(\d{2}):\d{2}:\d{2}.*", data["timestamp"])
        extract_hour = extract_hour.group(1)
        hour_value = f"{extract_hour}:00 - {(int(extract_hour)+1):02}:00 UTC" 
        ###
        updated_hour_list = list(hour["hour"] for hour in traffics_list)
        if not hour_value in updated_hour_list:
            traffics_list.append({"hour": hour_value, "requests": 1})
        else:
            hour_index = traffics_list.index(next(hour for hour in traffics_list if hour["hour"] == hour_value))
            traffics_list[hour_index]["requests"] += 1
    return sorted(traffics_list, key=lambda x: x["requests"], reverse=True)

def main():
    os.system("clear")
    file_type, file_path = input_file()

    # Fetch data from file and save as dictionary
    all_data_dict_list = extract_data_from_file(file_type, file_path)


    # Print Header
    print("Server Log Analysis Report")
    print("==========================")
    print("")

    # Calculate and print total_requests
    total_requests = total_number_of_requests(all_data_dict_list)
    print(f"Total requests: {total_requests}")
    print("")

    # Evaluate and print client IPs and their frequencies
    print("Tope 5 client IPs:")
    IP_frequencies_dict_list = IP_frequencies(all_data_dict_list)
    for i in range(len(IP_frequencies_dict_list)):
        print("   {:<16} - {:>3} requests".format(IP_frequencies_dict_list[i]["ip"], int(IP_frequencies_dict_list[i]["requests"])))
    print("")

    # Evaluate and print Status Codes and their frequencies
    print("Status Code Destribution:")
    status_frequencies_dict_list = status_code_destribution(all_data_dict_list)[1]
    for status in status_frequencies_dict_list:
        print("   {:<16} - {:>5} requests".format(list(status.keys())[0], int(list(status.values())[0])))
    print("")

    # Calculate and print Error Percentage
    error_percent = error_percentage(status_frequencies_dict_list)
    print(f"Error Percentage: {error_percent}")
    print("")

    # Evaluate and print Peak Traffic Hour
    traffics = sorted(hourly_traffics(all_data_dict_list), key = lambda x: x["requests"])
    print(f"Peak traffic hour: {traffics[0]["hour"]}")
    print("")

if __name__ == "__main__":
    main()

'''
#Sample Output

Server Log Analysis Report
=============================
Total requests: 12,458

Top 5 client IPs:
  192.168.1.10   - 830 requests
  10.0.0.45      - 701 requests
  203.0.113.5    - 643 requests
  172.16.0.8     - 522 requests
  198.51.100.22  - 498 requests

Status Code Distribution:
  2xx Success    - 10,432
  3xx Redirect   - 518
  4xx Client Err - 1,221
  5xx Server Err - 287

Error Percentage: 12.1%

Peak traffic hour: 14:00 - 15:00 UTC'''