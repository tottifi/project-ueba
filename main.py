from scripts.parser.frequency_connection_hour import frequency_connection_hour_get_array
from scripts.parser.profiling_ip_destination import profiling_ip_destination_get_array

from scripts.analysis.standard_deviation import StandardDeviation
from scripts.analysis.scoring_destination import ScoringDestination

"""
standard_deviation_filter = StandardDeviation({
    'file_log_out':'OUT_LOGS/standard_deviation_logs.txt',
    'coefficent_sd': 3
})

standard_deviation_filter.start(frequency_connection_hour_get_array())
"""

scoring_destination_filter = ScoringDestination({
    'file_log_out':'OUT_LOGS/scoring_destination_logs.txt',
    'coefficent_sd': 3,
    'floor_values': False,
    'show_errors': True
})

scoring_destination_filter.start(profiling_ip_destination_get_array())


