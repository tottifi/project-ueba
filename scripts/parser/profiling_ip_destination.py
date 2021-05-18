import sys
import re

"""
Create a csv for Profiling IP Destination from an all logs CSV

@param {String} logs_csv_path: Path to the csv file containing every logs
@param {String} profiling_csv_out_path: Path for the output csv
"""
def profiling_ip_destination_to_csv(logs_csv_path, profiling_csv_out_path):
    try:
        f = open(logs_csv_path)
        f.close()
    except FileNotFoundError:
        print("ERROR: No Full Logs CSV File Found")
        return

    print("INFO: Generating Profiling IP Destination CSV File")

    difference = 3600

    all_connections = []

    hour = 0

    last_time_range = -1
    last_day_checked = -1

    f = open(logs_csv_path, "r")
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

    print("INFO: Creating Profiling IP Destination CSV File")

    fout = open(profiling_csv_out_path, "w")

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

    print("INFO: Profiling IP Destination CSV File DONE")


"""
Create a csv for Profiling IP Destination from a premade CSV file

@param {String} profiling_csv_path: Path for the Profiling IP Destination CSV File

@returns:
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
def profiling_ip_destination_get_array(profiling_csv_path):
    try:
        f = open(profiling_csv_path)
        f.close()
    except FileNotFoundError:
        print("ERROR: No Profiling IP Destination CSV File Found")
        return []

    logs_array = []

    f = open(profiling_csv_path, "r")
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
