#!/usr/bin/env python3

import os, sys, re

def input_file():
    pass

def extract_data_from_file(file_type, file_path):
    pass

def total_number_of_requests(all_data_dict_list):
    pass

def IP_frequencies(all_data_dict_list):
    pass

def status_code_destribution(all_data_dict_list):
    pass

def error_percentage(status_dict_list):
    pass

def hourly_traffics(all_data_dict_list):
    pass

# Print Header
print("Server Log Analysis Report")
print("==============================")

file_status, file_type, file_path = input_file()

# Check if file is found, else exit
if file_status is not "OK":
    print("File not found!")
    sys.exit(1)
else:
    # Fetch data from file and save as dictionary
    all_data_dict_list = extract_data_from_file(file_type, file_path)

    # Calculate and print total_requests
    total_requests = total_number_of_requests(all_data_dict_list)
    print(f"Total requests: {total_requests}")

    # Evaluate and print client IPs and their frequencies
    print("Tope 5 client IPs:")
    IP_frequencies_dict_list = IP_frequencies(all_data_dict_list)
    for i in range(5):
        print("   {:<15} - {:,>3 } requests".format(IP_frequencies_dict_list[i]["IP"], IP_frequencies_dict_list[i]["frequency"]))

    # Evaluate and print Status Codes and their frequencies
    print("Status Code Destribution:")
    status_frequencies_dict_list = status_code_destribution(all_data_dict_list)
    for status in status_frequencies_dict_list:
        print("   {:<14} - {:,<10} requests".format(status_frequencies_dict_list["status"], status_frequencies_dict_list["frequency"]))

    # Calculate and print Error Percentage
    error_percent = error_percentage(status_frequencies_dict_list)
    print(f"Error Percentage: {error_percentage}%")

    # Evaluate and print Peak Traffic Hour
    traffics = hourly_traffics(all_data_dict_list)
    print(f"Peak traffic hour: {traffics[0]["Hour"]}:00 - {traffics[0]["Hour"]+1 if traffics[0]["Hour"] < 24 else 00}:00 UTC")

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