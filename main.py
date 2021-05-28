
from scripts.parser.logs_to_csv import logs_to_csv
from scripts.parser.frequency_connection_hour import frequency_connection_hour_get_array, frequency_connection_hour_to_csv
from scripts.parser.profiling_ip_destination import profiling_ip_destination_get_array, profiling_ip_destination_to_csv

from scripts.analysis.standard_deviation import StandardDeviation
from scripts.analysis.scoring_destination import ScoringDestination

filenames = []
for i in range(0, 30):
    filenames.append('LOGS/pflog.' + str(i) + '.bz2.log')

# Create a csv file filed with every logs
logs_to_csv(filenames, 'CSV/all_logs.csv')
# Create a csv file for Frequency Connection By Hour Parser
frequency_connection_hour_to_csv('CSV/all_logs.csv', 'CSV/frequency_connection_hour.csv')
# Create a csv file for the Profiling IP Destination Parser
profiling_ip_destination_to_csv('CSV/all_logs.csv', 'CSV/profiling_ip_destination.csv')

standard_deviation_filter = StandardDeviation({
    'silent': False,
    'file_log_out': 'OUT_LOGS/standard_deviation_logs.txt',
    'coefficent_sd': 3,
    'skip_zero': True
})

standard_deviation_filter.start(frequency_connection_hour_get_array('CSV/frequency_connection_hour.csv'))

scoring_destination_filter = ScoringDestination({
    'silent': False,
    'file_log_out': 'OUT_LOGS/scoring_destination_logs_nofunc.txt',
    'coefficent_sd': 3,
    'floor_values': False,
    'show_errors': True,
    'zero_errors': True
})

scoring_destination_filter.start(profiling_ip_destination_get_array('CSV/profiling_ip_destination.csv'))


