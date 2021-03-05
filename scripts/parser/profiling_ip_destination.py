import sys
import re

from scripts.parser.logs_to_csv import logs_to_csv


def profiling_ip_destination_to_csv():
    try:
        f = open('CSV/all_logs.csv')
        f.close()
    except FileNotFoundError:
        logs_to_csv()

    print("GENERATING PROFILING IP DESTINATION CSV")

    difference = 3600

    all_connections = []

    hour = 0

    last_time_range = -1
    last_day_checked = -1

    f = open('CSV/all_logs.csv', "r")
    # Skip Header CSV
    f.readline()

    for line in f:
        # :-1 to skip carriage return
        line_splitted = line[:-1].split(',')

        if last_day_checked != int(line_splitted[0]):
            last_day_checked = int(line_splitted[0])
            print('INFO: Checking day ' + str(last_day_checked))

        time = int(line_splitted[0]) * 3600 * 24 + int(line_splitted[1]) * 3600 + int(line_splitted[2]) * 60 + int(
            line_splitted[3])

        if last_time_range == -1 or last_time_range + difference < time:
            last_time_range = time
            hour += 1
            all_connections.append({})

        ip_dest = line_splitted[7]
        port_dest = line_splitted[8]
        protocol = line_splitted[9]

        if not (ip_dest in all_connections[-1]):
            all_connections[-1][ip_dest] = {}

        if not (port_dest in all_connections[-1][ip_dest]):
            all_connections[-1][ip_dest][port_dest] = {}

        if not (protocol in all_connections[-1][ip_dest][port_dest]):
            all_connections[-1][ip_dest][port_dest][protocol] = 1
        else:
            all_connections[-1][ip_dest][port_dest][protocol] += 1

    f.close()

    print("INFO: Creating CSV File")

    fout = open('CSV/profiling_ip_destination.csv', "w")

    fout.write('hour,ip_dest,port_dest,protocol,number_connections\n')

    hour = 0
    for connections in all_connections:
        for ip_dest in connections:
            for port_dest in connections[ip_dest]:
                for protocol in connections[ip_dest][port_dest]:
                    fout.write(str(hour) + ',')
                    fout.write(ip_dest + ',')
                    fout.write(port_dest + ',')
                    fout.write(protocol + ',')
                    fout.write(str(connections[ip_dest][port_dest][protocol]))
                    fout.write('\n')
        print("Hour " + str(hour) + " Checked")
        hour += 1

    fout.close()

"""
    [
        [
            <int> Hour,
            <string> IP Destination, 
            <string> Port Destination, 
            <string> Protocol,
            <int> Number of connections with previous values
        ], 
        ...
    ]
"""
def profiling_ip_destination_get_array():
    try:
        f = open('CSV/profiling_ip_destination.csv')
        f.close()
    except FileNotFoundError:
        profiling_ip_destination_to_csv()

    logs_array = []

    f = open('CSV/profiling_ip_destination.csv', "r")
    # Skip Header CSV
    f.readline()

    for line in f:
        line_splitted = line.split(',')

        logs_array.append([])

        for element in line_splitted:
            logs_array[-1].append(element)

        logs_array[-1][0] = int(logs_array[-1][0])
        logs_array[-1][-1] = int(logs_array[-1][-1])

    f.close()

    return logs_array


if __name__ == "__main__":
    profiling_ip_destination_to_csv()
