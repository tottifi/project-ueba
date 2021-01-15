import sys
import re

from scripts.parser.logs_to_csv import logs_to_csv


def frequency_connection_hour_to_csv():
    try:
        f = open('CSV/all_logs.csv')
        f.close()
    except FileNotFoundError:
        logs_to_csv()

    print("GENERATING FREQUENCY CONNECTION BY HOUR CSV")

    print("INFO: Calculating Frequency")

    difference = 3600

    all_ip = []
    all_ip_by_times = []

    last_time_range = -1
    last_day_checked = -1

    f = open('CSV/all_logs.csv', "r")
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

    print("INFO: Creating CSV File")

    fout = open('CSV/frequency_connection_hour.csv', "w")

    fout.write('ip')
    for i in range(0, len(all_ip_by_times)):
        fout.write(',hour' + str(i))
    fout.write('\n')

    # Uniquement Print
    print("Total d'ip: " + str(len(all_ip)))
    print_index = 0
    print_index2 = 0
    # Fin Uniquement Print

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


def frequency_connection_hour_get_array():
    try:
        f = open('CSV/frequency_connection_hour.csv')
        f.close()
    except FileNotFoundError:
        frequency_connection_hour_to_csv()

    logs_array = []

    f = open('CSV/frequency_connection_hour.csv', "r")
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
