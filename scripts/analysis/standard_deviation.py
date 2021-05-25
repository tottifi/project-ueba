import json
import math


class StandardDeviation:

    def __init__(self, options):
        self.silent = False
        if 'silent' in options:
            self.silent = options['silent']

        self.file_log_out = None
        if 'file_log_out' in options:
            self.file_log_out = options['file_log_out']

        self.coefficent_standard_deviation = 3
        if 'coefficent_sd' in options:
            self.coefficent_standard_deviation = int(options['coefficent_sd'])

        self.floor_values = False
        if 'floor_values' in options:
            self.floor_values = options['floor_values']

        self.skip_zero = True
        if 'skip_zero' in options:
            self.skip_zero = True if options['skip_zero'] else False

    """
    Logs must be passed as 
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
    def start(self, logs):
        if not self.silent:
            print('INFO: Starting Standard Deviation Analysis')

        results = []

        for ip_array in logs:
            total_to_skip = 0
            mean = 0
            for i in range(1, len(ip_array)):
                if self.skip_zero and ip_array[i] == 0:
                    total_to_skip += 1
                    continue
                mean += ip_array[i]
            mean /= len(ip_array) - 1 - total_to_skip

            standard_deviation = 0
            for i in range(1, len(ip_array)):
                if self.skip_zero and ip_array[i] == 0:
                    continue
                standard_deviation += (ip_array[i] - mean) * (ip_array[i] - mean)
            standard_deviation /= len(ip_array) - 1 - total_to_skip
            standard_deviation = math.sqrt(standard_deviation)

            warning_ip = {
                'ip': ip_array[0],
                'mean': mean,
                'sd': standard_deviation,
                'warnings': []
            }

            if self.floor_values:
                warning_ip['mean'] = math.floor(mean)
                warning_ip['sd'] = math.floor(standard_deviation)

            for i in range(1, len(ip_array)):
                if self.skip_zero and ip_array[i] == 0:
                    continue

                is_error = False
                type_error = ''
                if ip_array[i] > mean and ip_array[i] > mean + self.coefficent_standard_deviation * standard_deviation:
                    is_error = True
                    type_error = 'HIGH'
                elif ip_array[i] < mean and ip_array[i] < mean - self.coefficent_standard_deviation * standard_deviation:
                    is_error = True
                    type_error = 'LOW'

                if is_error:
                    warning = {
                        'type': type_error,
                        'total': ip_array[i],
                        'hour': i
                    }
                    warning_ip['warnings'].append(warning)

            if len(warning_ip['warnings']) > 0:
                results.append(warning_ip)

        if self.file_log_out:
            if not self.silent:
                print("INFO: Logging data...")
            f = open(self.file_log_out, 'w')
            f.write(json.dumps(results))
            f.close()

        return results

