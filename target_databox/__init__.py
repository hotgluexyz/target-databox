#!/usr/bin/env python3
import json
import sys
import argparse
import base64
import pandas as pd
import gluestick as gs
import logging
from databox import Client

logger = logging.getLogger("target-databox")
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def load_json(path):
    with open(path) as f:
        return json.load(f)


def parse_args():
    '''Parse standard command-line args.
    Parses the command-line arguments mentioned in the SPEC and the
    BEST_PRACTICES documents:
    -c,--config     Config file
    -s,--state      State file
    -d,--discover   Run in discover mode
    -p,--properties Properties file: DEPRECATED, please use --catalog instead
    --catalog       Catalog file
    Returns the parsed args object from argparse. For each argument that
    point to JSON files (config, state, properties), we will automatically
    load and parse the JSON file.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config',
        help='Config file',
        required=True)

    args = parser.parse_args()
    if args.config:
        setattr(args, 'config_path', args.config)
        args.config = load_json(args.config)

    return args

def load_data(config):
    # Read the passed CSV
    entities = gs.read_csv_folder(config['input_path'])
    return entities


def post_data(config, data):
    client = Client(config['access_token'])

    for entity_name in data:
        entity = data[entity_name]
        formatted_rows = []

        for index, row in entity.iterrows():
            formatted_rows.append({'key': f'{entity_name}.{row["key"]}', 'value': row['value'], 'date': row['date']})

        logger.debug(f"Exporting {json.dumps(formatted_rows)}")
        # Push formatted rows to Databox
        client.insert_all(formatted_rows)
        logger.debug(f"Exported {entity_name}")


def upload(config):
    # Load CSVs to post
    data = load_data(config)
    logger.debug(f"Exporting {list(data.keys())}...")

    # Post CSV data to Databox
    post_data(config, data)


def main():
    # Parse command line arguments
    args = parse_args()

    # Upload the 
    upload(args.config)


if __name__ == "__main__":
    main()
