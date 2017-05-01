# tap-csv

A [Singer](https://singer.io) tap for extracting data from a CSV file.

## Limitations

This is a fairly brittle implementation of a CSV reader, but it gets 
the job done for tasks where you file structure is highly predictable.

The input files must be a traditionally-delimited CSV (commas separated
columns, newlines indicate new rows, double quoted values) as defined 
by the defaults to the python `csv` library.

Paths to local files and the names of their corresponding entities are
specified in the config file, and each file must contain a header row
including the names of the columns that follow.

Perhaps the greatest limitation of this implementation is that it
assumes all incoming data is a string. Future iterations could
intelligently identify data types based on a sampling of rows or
allow the user to provide that information.


## Install

Clone this repository, and then:

```bash
› python setup.py install
```

## Run

#### Run the application

```bash

python tap_csv.py -c config.json

```

Where `config.json` contains an array called `files` that consists of dictionary objects detailing each destination table to be passed to Singer. Each of those entries contains: 
* `entity`: The entity name to be passed to singer (i.e. the table)
* `path`: Local path to the file to be ingested. Note that this may be a directory, in which case all files in that directory and any of its subdirectories will be recursively processed
* `keys`: The names of the columns that constitute the unique keys for that entity

Example:

```json
{
	"files":	[ 	
					{	"entity" : "leads",
						"file" : "/path/to/leads.csv",
						"keys" : ["Id"]
					},
					{	"entity" : "opportunities",
						"file" : "/path/to/opportunities.csv",
						"keys" : ["Id"]
					}
				]
}
```

and `state.json` is a file containing only the value of the last state
message, which again is moot for this tap because it is only run on
individual files a single time.


