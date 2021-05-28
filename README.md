# Projet UEBA

This GitHub is made to supports scripts which could be used for the [Darwin Project](https://github.com/VultureProject/darwin).

Examples for following scripts are made in the main file `main.py`.

Two kinds of scripts are made:

## Parser Scripts

Parsers are meant to parse logs into more readables CSV formats.

### `logs_to_csv.py`

This script is used to change main logs into one single CSV file:

```python
logs_to_csv(logs_paths, csv_out_path)
```

* `logs_paths`: A String Array with all differents logs paths to concat into one single csv
* `csv_out_path`: A String Path for the output csv

### `frequency_connection_hour.py`

Scripts to create a Frequency Connection by Hours CSV file from Source IPs.

```python
frequency_connection_hour_to_csv(logs_csv_path, frequency_connection_csv_out_path)
```

* `logs_csv_path`: A String Path to the csv file containing every logs
* `frequency_connection_csv_out_path`: A String Path for the output csv

Generating an array from the generated CSV :

```python
frequency_connection_hour_get_array(frequency_connection_csv_path)
```

* `frequency_connection_csv_path`: A String Path for the csv previously generated

Array will be in this format :

```
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
```

### `profiling_ip_destination.py`

Scripts to create a Total number of connection Profiling by IP/Port/Protocol every hour CSV file from Destinations IPs.

```python
profiling_ip_destination_to_csv(logs_csv_path, profiling_csv_out_path)
```

* `logs_csv_path`: A String Path to the csv file containing every logs
* `profiling_csv_out_path`: A String Path for the output csv

Generating an array from the generated CSV :

```python
profiling_ip_destination_get_array(profiling_csv_path)
```

* `profiling_csv_path`: A String Path for the csv previously generated

Array will be in this format :

```
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
```

## Analysis Scripts

Analysis scripts are meant to gives analysts some infos regarding which IP or Time range should be checked given our calculated warnings.

### `standard_deviation.py`

Script which is checking which hours are deviating from the usual number of connections for each Source IP.

```python
standard_deviation_filter = StandardDeviation({
    'silent': False,
    'file_log_out': 'OUT_LOGS/standard_deviation_logs.txt',
    'coefficent_sd': 3,
    'floor_values': False,
    'skip_zero': True
})

standard_deviation_filter.start(logs)
```

We create an object for the filter and initialize it with options :
-	`silent` : Boolean preventing the console logging its infos
-	`file_log_out` : String path to the file where logs will be outputed
-	`coefficient_sd` : Number for the standard deviation coefficient for which we will detect errors
-	`floor_values` : Boolean flooring values for standard deviations and means
-	`skip_zero` : Boolean so the script skip hours with zero values

We will then be able to start the algorithm with `.start(logs)` which will then output its results in a file if `file_log_out` is set and returned from the function.

Logs must be passed as 
```
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
```

### `scoring_destination.py`

Script which is giving scores of errors to each hours given the total number of connections for each couples of IP/Port/Protocol.

```python
scoring_destination_filter = ScoringDestination({
    'silent': False,
    'file_log_out': 'OUT_LOGS/scoring_destination_logs_nofunc.txt',
    'coefficent_sd': 3,
    'floor_values': False,
    'show_errors': True,
    'zero_errors': True
})

scoring_destination_filter.start(logs)
```

We create an object for the filter and initialize it with options :
-	`silent` : Boolean preventing the console logging its infos
-	`file_log_out` : String path to the file where logs will be outputed
-	`coefficient_sd` : Number for the standard deviation coefficient for which we will detect errors
-	`floor_values` : Boolean flooring values for standard deviations and means
-	`show_errors` : Boolean which allow the script to logs more accurately why and how scores are calculated
- `zero_errors` : Boolean which put logs for every hours even for which score is still 0

We will then be able to start the algorithm with `.start(logs)` which will then output its results in a file if `file_log_out` is set and returned from the function.

Logs must be passed as 
```
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
```
