import sys
import re

from scripts.parser.logs_to_csv import logs_to_csv

"""
Create a csv for Profiling IP Destination from an all logs CSV

@param {String} logs_csv_path: Path to the csv file containing every logs
@param {String} frequency_connection_csv_out_path: Path for the output csv
"""
def frequency_connection_hour_to_csv(logs_csv_path, frequency_connection_csv_out_path):
    try:
        f = open(logs_csv_path)
        f.close()
    except FileNotFoundError:
        print("ERROR: No Full Logs CSV File Found")
        return

    print("INFO: Generating Frequency Connection By Hour CSV File")

    difference = 3600

    all_ip = []
    all_ip_by_times = []

    last_time_range = -1
    last_day_checked = -1

    f = open(logs_csv_path, "r")
    # Skip Header CSV
    f.readline()

    for line in f:
        line_splitted = line.split(',')

        if last_day_checked != int(line_splitted[0]):
            last_day_checked = int(line_splitted[0])
            print('INFO: Checking day ' + str(last_day_checked))

        time = int(line_splitted[0]) * 3600 * 24 + int(line_splitted[1]) * 3600 + int(line_splitted[2]) * 60 + int(
            line_splitted[3])

        if last_time_range == -1 or last_time_range + difference < time:
            last_time_range = time
            all_ip_by_times.append({})

        ip_source = line_splitted[5]

        if not (ip_source in all_ip_by_times[-1]):
            all_ip_by_times[-1][ip_source] = 1
        else:
            all_ip_by_times[-1][ip_source] += 1

        if not (ip_source in all_ip):
            all_ip.append(ip_source)

    f.close()

    print("INFO: Creating Frequency Connection By Hour CSV File")

    fout = open(frequency_connection_csv_out_path, "w")

    fout.write('ip')
    for i in range(0, len(all_ip_by_times)):
        fout.write(',hour' + str(i))
    fout.write('\n')

    # Print
    print("IPs to check: " + str(len(all_ip)))
    print_index = 0
    print_index2 = 0

    for ip in all_ip:
        fout.write(ip)
        print_index += 1
        if print_index == 100:
            print_index = 0
            print_index2 += 1 * 100
            print("IP " + str(print_index2) + " Checked")
        for day in all_ip_by_times:
            if not (ip in day):
                fout.write(',0')
            else:
                fout.write(',' + str(day[ip]))
        fout.write('\n')

    fout.close()

    print("INFO: Frequency Connection By Hour CSV File DONE")

"""
Create a csv for Frequency Connection By Hour from a premade CSV file

@param {String} frequency_connection_csv_path: Path for the Frequency Connection By Hour CSV File

@returns:
    [
        [
            <string> IP, 
            <int> Total connections on time range 0, 
            <int> Total connections on time range 1, 
            ...
            <int> Total connections on time range MAX
        ], 
    ...
    ]
"""
def frequency_connection_hour_get_array(frequency_connection_csv_path):
    try:
        f = open(frequency_connection_csv_path)
        f.close()
    except FileNotFoundError:
        print("ERROR: No Frequency Connection By Hour CSV File Found")
        return []

    logs_array = []

    f = open(frequency_connection_csv_path, "r")
    # Skip Header CSV
    f.readline()

    for line in f:
        line_splitted = line.split(',')

        logs_array.append([])
        logs_array[-1].append(line_splitted.pop(0))

        for element in line_splitted:
            logs_array[-1].append(int(element))

    f.close()

    return logs_array


if __name__ == "__main__":
    frequency_connection_hour_to_csv()
