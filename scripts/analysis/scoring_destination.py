import json
import math

"""
  Calcul d'un score d'erreurs par heure selon plusieurs criteres (Ip inconnue, port inconnu contacte, ...) vers l'IP de destination
  Ce score est ensuite multiplié au nombre d'erreurs calculées à partir d'une déviation standard sur cette meme heure.

  Nous entrainons d'abord le programme avec plusieurs heures de logs pour savoir les protocoles, ports et IP communes et ainsi 
  determiner quand nous aurons des changements par rapport a cela.

  Nous fournissons ensuite plusieurs autres heures a etudier et le resultat s'etablira sur ces logs ci.
"""
class ScoringDestination:

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

        self.zero_errors = False
        if 'zero_errors' in options:
            self.zero_errors = options['zero_errors']

        self.show_errors = True
        if 'show_errors' in options:
            self.show_errors = options['show_errors']
    

    """
    Logs must be passed as 
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
    def start(self, logs):
        if not self.silent:
            print('INFO: Calculating Standard Deviations...')
        trained = {}

        total_hours = 0
        last_hour = -1
        for hour_log in logs:
            if last_hour != hour_log[0]:
                last_hour = hour_log[0]
                total_hours += 1

            if hour_log[1] not in trained:
                trained[hour_log[1]] = {}
            if hour_log[2] not in trained[hour_log[1]]:
                trained[hour_log[1]][hour_log[2]] = {}
            if hour_log[3] not in trained[hour_log[1]][hour_log[2]]:
                trained[hour_log[1]][hour_log[2]][hour_log[3]] = {
                    'mean': 0,
                    'sd': 0,
                    'values': []
                }
            trained[hour_log[1]][hour_log[2]][hour_log[3]]['mean'] += hour_log[4]
            trained[hour_log[1]][hour_log[2]][hour_log[3]]['values'].append(hour_log[4])

        for ip_dest in trained:
            for port_dest in trained[ip_dest]:
                for protocol in trained[ip_dest][port_dest]:
                    trained[ip_dest][port_dest][protocol]['mean'] /= total_hours
                    
        for ip_dest in trained:
            for port_dest in trained[ip_dest]:
                for protocol in trained[ip_dest][port_dest]:
                    mean = trained[ip_dest][port_dest][protocol]['mean']
                    sd = 0

                    total_values = len(trained[ip_dest][port_dest][protocol]['values'])
                    for value in trained[ip_dest][port_dest][protocol]['values']:
                        sd += (value - mean) * (value - mean)
                    sd /= total_hours
                    sd = math.sqrt(sd)
                    
                    trained[ip_dest][port_dest][protocol]['sd'] = sd

        if not self.silent:
            print('INFO: Calculating scores and errors...')
        last_hour = -1
        results = []
        for hour_log in logs:
            while last_hour < hour_log[0]:
                last_hour += 1
                if last_hour == hour_log[0] or self.zero_errors:
                    results.append({
                        'hour': last_hour,
                        'score': 0
                    })
                    if self.show_errors:
                        results[-1]['errors'] = []

            log_sd = trained[hour_log[1]][hour_log[2]][hour_log[3]]['sd']
            log_mean = trained[hour_log[1]][hour_log[2]][hour_log[3]]['mean']

            is_error = False
            if hour_log[4] > log_mean and hour_log[4] > log_mean + self.coefficent_standard_deviation * log_sd:
                is_error = True
            elif hour_log[4] < log_mean and hour_log[4] < log_mean - self.coefficent_standard_deviation * log_sd:
                is_error = True

            if is_error:
                no_zero_sd = self.coefficent_standard_deviation * log_sd if log_sd != 0 else 0.1
                results[-1]['score'] += (abs(hour_log[4] - log_mean) - self.coefficent_standard_deviation * log_sd) / no_zero_sd

                if self.show_errors:
                    warning = {
                        'ip': hour_log[1],
                        'port': hour_log[2],
                        'protocol': hour_log[3],
                        'total': hour_log[4],
                        'mean': log_mean,
                        'sd': log_sd
                    }

                    if self.floor_values:
                        warning['mean'] = math.floor(mean)
                        warning['sd'] = math.floor(sd)

                    results[-1]['errors'].append(warning)

        if self.floor_values:
            for element in results:
                element['score'] = math.floor(element['score'])

        if self.file_log_out:
            if not self.silent:
                print("INFO: Logging data...")
            f = open(self.file_log_out, 'w')
            f.write(json.dumps(results))
            f.close()

        return results
        