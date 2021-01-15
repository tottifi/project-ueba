from scripts.parser.frequency_connection_hour import frequency_connection_hour_get_array

from scripts.analysis.standard_deviation import StandardDeviation

standard_deviation_filter = StandardDeviation({
    'logging': True,
    'coefficent_sd': 3
})

standard_deviation_filter.start(frequency_connection_hour_get_array())


