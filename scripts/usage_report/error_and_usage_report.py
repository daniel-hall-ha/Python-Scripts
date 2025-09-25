#!/usr/bin/env python3

import os, sys, re, csv
from pathlib import Path
import datetime

def main():

        output_file_path = os.path.join(Path(__file__).parents[2], "data", "usage_report")

        log_file = sys.argv[1]

        error_message = []
        usage_statistics = [] 

        with open(log_file, 'r') as file:
                logs = file.readlines()    
                logs = [log.strip() for log in logs]
                pattern = r"(INFO|ERROR) ([\w ]+) \(([a-z]+)\)"
                for log in logs:
                        result = re.search(pattern, log)
                        if result:
                                if any(d.get("Error")==result[2] for d in error_message):
                                        index = next((i for i, d in enumerate(error_message) if d.get("Error") == result[2]), -1)
                                        error_message[index]["Count"] += 1
                                        print("Found error {} again ….".format(result[2]))
                                else:
                                        error_message.append({"Error":result[2], "Count": 1})   
                                        print("Found error {}  for the first time ….".format(result[2]))
                                if any(d.get("Username")==result[3] for d in usage_statistics):
                                        index = next((i for i,d in enumerate(usage_statistics) if d.get("Username")==result[3]),-1) 
                                        usage_statistics[index]["INFO"]+=1 if result[1] == "INFO" else 0
                                        usage_statistics[index]["ERROR"]+=1 if result[1] == "ERROR" else 0
                                        print("Found user {} again with {}".format(result[3],result[1]))
                                else:
                                        info = 1 if result[1] == "INFO" else 0
                                        error = 1 if result[1] == "ERROR" else 0
                                        usage_statistics.append({"Username": result[3], "INFO": info, "ERROR": error})
                                        print("Found user {} for the first time with {}".format(result[3],result[1]))
                error_message = sorted(error_message, key=lambda x: x["Count"], reverse=True)
                usage_statistics = sorted(usage_statistics, key=lambda x: x["Username"])
        file.close()

        output_file_suffix = datetime.datetime.now().strftime("%d%m%Y%H%M%S")

        with open(f"error_report_{output_file_suffix}.csv", 'w', newline="") as file:
                dict_writer = csv.DictWriter(file, fieldnames=error_message[0].keys())
                dict_writer.writeheader()
                dict_writer.writerows(error_message)
        file.close()

        print("error_message_report.csv has been saved to ", output_file_path)

        with open(f"usage_statistics_{output_file_suffix}.csv", 'w', newline="") as file:
                dict_writer = csv.DictWriter(file, fieldnames=usage_statistics[0].keys())
                dict_writer.writeheader()
                dict_writer.writerows(usage_statistics)
        file.close()

        print(f"usage_statistics_report.csv has been saved to ", output_file_path)

if __name__ == "__main__":
        main()