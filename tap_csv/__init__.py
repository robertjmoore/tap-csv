#!/usr/bin/env python3

import singer
import csv
import sys
import argparse
import json
import os
import copy


REQUIRED_CONFIG_KEYS = ['files']
STATE = {}
CONFIG = {}

logger = singer.get_logger()

def write_schema_from_header(entity, header, keys):
    schema =    {
                    "type": "object",
                    "properties": {}
                }
    header_map = []
    for column in header:
        #for now everything is a string; ideas for later:
        #1. intelligently detect data types based on a sampling of entries from the raw data
        #2. by default everything is a string, but allow entries in config.json to hard-type columns by name
        schema["properties"][column] = {"type": "string" } 
        header_map.append(column)

    singer.write_schema(entity, schema, keys) 

    return header_map

def process_file(fileInfo):
    #determines if file in question is a file or directory and processes accordingly
    if not os.path.exists(fileInfo["file"]):
        logger.info("Directory " + fileInfo["file"] + " does not exist, skipping")
        return
    if os.path.isdir(fileInfo["file"]):
        fileInfo["file"] = os.path.normpath(fileInfo["file"]) + os.sep #ensures directories end with trailing slash
        logger.info("Syncing all CSV files in directory '" + fileInfo["file"] + "' recursively")
        for filename in os.listdir(fileInfo["file"]):
            subInfo = copy.deepcopy(fileInfo)
            subInfo["file"] = fileInfo["file"] + filename
            process_file(subInfo) #recursive call
    else: 
        sync_file(fileInfo)

def sync_file(fileInfo):
    if fileInfo["file"][-4:] != ".csv":
        logger.info("Skipping non-csv file '" + fileInfo["file"] + "'")
        return

    logger.info("Syncing entity '" + fileInfo["entity"] + "' from file: '" + fileInfo["file"] + "'")
    with open(fileInfo["file"], "r") as f:
        needsHeader = True
        reader = csv.reader(f)
        for row in reader:
            if(needsHeader):
                header_map = write_schema_from_header(fileInfo["entity"], row, fileInfo["keys"])
                needsHeader = False
            else:
                record = {}
                for index, column in enumerate(row):
                    record[header_map[index]] = column
                if len(record) > 0: #skip empty lines
                    singer.write_record(fileInfo["entity"], record)

    singer.write_state(STATE) #moot instruction, state always empty

def parse_args(required_config_keys):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file', required=True)
    parser.add_argument('-s', '--state', help='State file')
    args = parser.parse_args()

    config = load_json(args.config)
    check_config(config, required_config_keys)

    if args.state:
        state = load_json(args.state)
    else:
        state = {}

    return config, state

def load_json(path):
    with open(path) as f:
        return json.load(f)

def check_config(config, required_keys):
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise Exception("Config is missing required keys: {}".format(missing_keys))


def do_sync():
    logger.info("Starting sync")
    for fileInfo in CONFIG['files']:
        process_file(fileInfo)
    logger.info("Sync completed")


def main():
    config, state = parse_args(REQUIRED_CONFIG_KEYS)
    CONFIG.update(config)
    STATE.update(state)
    do_sync()


if __name__ == '__main__':
    main()
