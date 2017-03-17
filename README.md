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

Where `config.json` contains an array of local filepaths to be ingested.

```json
{
	"files":	[ 	
					{	"entity" : "leads",
						"file" : "/path/to/leads.csv" 
					},
					{	"entity" : "opportunities",
						"file" : "/path/to/opportunities.csv" 
					}
				]
}
```

and `state.json` is a file containing only the value of the last state
message, which again is moot for this tap because it is only run on
individual files a single time.

---

Copyright &copy; 2017 Stitch
