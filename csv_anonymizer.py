"""
CSV anonymization module.
Handles reading, anonymizing, and writing CSV files.
"""

import csv
from typing import List, Iterator
from anonymizer import anonymize_value


def anonymize_rows(rows: Iterator, selectors: List, faker, template_env) -> Iterator:
    """
    Anonymize rows based on selectors.
    
    Args:
        rows: Iterator of row lists
        selectors: List of Selector objects
        faker: Faker instance
        template_env: Jinja2 environment
        
    Yields:
        Anonymized rows
    """
    for row in rows:
        context = {}
        for selector in selectors:
            if selector.column is None:
                raise ValueError(f'No column given in selector {selector}')

            column_index = int(selector.column)
            if column_index < len(row):
                if len(row[column_index].strip()) > 0:
                    original_value = row[column_index].strip().replace('\n', '')
                    anonymized_value = anonymize_value(
                        selector, original_value, context, faker, template_env
                    )
                    row[column_index] = anonymized_value
        yield row


def anonymize_csv(source_file_name: str, target_file_name: str, selectors: List, 
                  header_lines: int, encoding: str, delimiter: str, faker, template_env) -> int:
    """
    Anonymize a CSV file.
    
    Args:
        source_file_name: Path to source CSV
        target_file_name: Path to target CSV
        selectors: List of Selector objects
        header_lines: Number of header lines to skip
        encoding: File encoding
        delimiter: CSV delimiter
        faker: Faker instance
        template_env: Jinja2 environment
        
    Returns:
        Number of rows anonymized
    """
    counter = 0
    with open(source_file_name, 'r', encoding=encoding, newline=None) as inputfile:
        with open(target_file_name, 'w', encoding=encoding) as outputfile:
            reader = csv.reader(inputfile, delimiter=delimiter)
            writer = csv.writer(outputfile, delimiter=delimiter, lineterminator='\n')

            # Write header lines
            skip_lines = header_lines
            while skip_lines > 0:
                writer.writerow(next(reader))
                skip_lines -= 1
            
            # Anonymize and write data
            for row in anonymize_rows(reader, selectors, faker, template_env):
                writer.writerow(row)
                counter += 1
    return counter
