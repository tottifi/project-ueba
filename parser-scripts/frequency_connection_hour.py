import sys
import re

last = -1
last_day_checked = -1
difference = 3600
precedent_time = 0
base = 0
all_ip = []
all_ip_by_times = []

def frequency_connection(filepath):
  global last
  global base
  global precedent_time
  global last_day_checked
  
  f = open(filepath, "r")
  # Skip Header CSV
  f.readline()

  for line in f:
    line_splitted = line.split(',')

    if last_day_checked != int(line_splitted[0]):
      last_day_checked = int(line_splitted[0])
      print('INFO: Checking day ' + str(last_day_checked))

    time = int(line_splitted[1]) * 3600 + int(line_splitted[2]) * 60 + int(line_splitted[3])
    time += base

    if (precedent_time > time):
      base += 24 * 3600
      time += 24 * 3600
    precedent_time = time

    if (last == -1 or last + difference < time):
      last = time
      all_ip_by_times.append({})

    ip_source = line_splitted[5]

    if not (ip_source in all_ip_by_times[-1]):
      all_ip_by_times[-1][ip_source] = 1
    else:
      all_ip_by_times[-1][ip_source] += 1

    if not (ip_source in all_ip):
      all_ip.append(ip_source)
  
  f.close()


def create_csv():
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



def main():
  frequency_connection('CSV/all_logs.csv')
  
  create_csv()



if __name__ == "__main__":
  main()