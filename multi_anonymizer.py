#!/usr/bin/env python3
"""
Command line interface for CSV Anonymizer.
"""

import argparse
import os
import sys
import time
import shutil
import glob2 as glob
from typing import Dict, List
from jinja2 import Environment
from faker import Factory

from selector import Selector
from source import Source
from utils import find_rightmost_colon, print_selector_map
from csv_anonymizer import anonymize_csv
from anonymizer import unidecode_filter

# Import optional modules
try:
    from lxml import etree
    xml_available = True
except ImportError:
    xml_available = False

try:
    from sqlalchemy import create_engine, select, update, MetaData, Table, bindparam
    sql_available = True
except ImportError:
    sql_available = False

try:
    import json
    from jsonpath_ng import jsonpath, parse
    json_available = True
except ImportError:
    json_available = False


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Anonymize columns of one ore more csv files',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', '--input', nargs='+', action='extend', dest='input',
        help="inputfile1:(type=number,column=0) [inputfile2:(type=number,column=0)] for csv"
    )
    parser.add_argument(
        '-t', '--type', dest='type', default='number',
        help='name, first_name, last_name, email, zip, city, address, number, ...'
    )
    parser.add_argument(
        '-e', '--encoding', dest='encoding', default='ISO-8859-15',
        help='file encoding. Default is ISO-8859-15'
    )
    parser.add_argument(
        '-d', '--delimiter', dest='delimiter', default=';',
        help='CSV delimiter. Default is semicolon.'
    )
    parser.add_argument(
        '-l', '--locale', dest='locale', default='de_DE',
        help='locale for fake data. Default is de_DE'
    )
    parser.add_argument(
        '-o', '--overwrite', dest='overwrite', action='store_true',
        help='overwrite original file'
    )
    parser.add_argument(
        '-j', '--ignore-missing-file', dest='ignoreMissingFile', action='store_true',
        help='ignore missing files'
    )
    parser.add_argument(
        '--header-lines', dest='headerLines', default='0',
        help='number of header lines to skip, default = 0'
    )
    parser.add_argument(
        '--namespace', nargs='+', dest='namespace',
        help='XML namespaces for xpath'
    )
    return parser


def main():
    """Main entry point for CLI."""
    parser = parse_args()
    ARGS = parser.parse_args()

    if ARGS.input is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    template_env = Environment()
    template_env.filters['unidecode'] = unidecode_filter
    FAKER = Factory.create(ARGS.locale)

    if ARGS.delimiter == "\t":
        print('Detected tab as delimiter')
    delimiter = ARGS.delimiter

    source_selector_map = {}

    for input_source in ARGS.input:
        split_index = find_rightmost_colon(input_source)
        if split_index is None:
            print('Syntax error: no colon found!')
            sys.exit(2)
        input_name = input_source[:split_index]
        selector_string = input_source[split_index+1:]
        selector_string = selector_string.replace('::', ':')

        source_is_database = '://' in input_name

        if source_is_database:
            inputs_to_read = [input_name]
        else:
            inputs_to_read = glob.glob(input_name)

        if len(inputs_to_read) == 0 and not ARGS.ignoreMissingFile:
            print('no input sources found: %s' % input_name)
            sys.exit(1)

        for source_name in inputs_to_read:
            selector = Selector(selector_string, ARGS.type)

            if selector.input_type is None:
                if source_name.endswith('.csv'):
                    selector.input_type = 'csv'
                elif source_name.endswith('.json'):
                    selector.input_type = 'json'
                elif source_name.endswith('.xml'):
                    selector.input_type = 'xml'
                if '://' in source_name:
                    selector.input_type = 'db'

            source = Source(source_name, None)
            if selector.input_type == "db":
                source.sub_source = selector.table

            if source not in source_selector_map.keys():
                source_selector_map[source] = []

            source_selector_map[source].append(selector)

    print('All anonymizations:')
    print_selector_map(source_selector_map)

    total_counter = 0
    start_time = time.process_time()

    for source in source_selector_map.keys():
        selectors = source_selector_map[source]
        print(f"Processing '{source.name}' with the selectors:")
        for selector in selectors:
            print(f'  {selector}')

        counter = 0
        source_is_database = '://' in source.name

        if not source_is_database:
            target = source.name + '_anonymized'
            if os.path.isfile(source.name):
                print(f'anonymizing file {source.name} to {target}')

                if selectors[0].input_type == 'csv':
                    counter = anonymize_csv(
                        source.name, target, selectors,
                        int(ARGS.headerLines), ARGS.encoding, delimiter,
                        FAKER, template_env
                    )

                if ARGS.overwrite:
                    print(f'overwriting original file {source.name}!')
                    shutil.move(src=target, dst=source.name)
            else:
                if ARGS.ignoreMissingFile:
                    print(f'ignoring missing file {source.name}')
                else:
                    print(f'file {source.name} does not exist!')
                    sys.exit(1)

        total_counter += counter

    end_time = time.process_time()
    print(f'Anonymized {total_counter} values in {(end_time - start_time):.2f}s')


if __name__ == '__main__':
    main()
