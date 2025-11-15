"""
Selector module for CSV Anonymizer.
Defines the Selector class for parsing and storing anonymization parameters.
"""

import sys
import re


class Selector:
    """
    Represents a selector for anonymization with various parameters.
    
    Attributes:
        data_type: Type of data to anonymize (name, email, number, etc.)
        input_type: Type of input (csv, xml, json, db)
        table: Database table name
        column: Column name or index
        xpath: XPath selector for XML
        jsonpath: JSONPath selector for JSON
        regexp: Regular expression for partial matching
        template: Jinja2 template for output formatting
        min: Minimum value for number generation
        max: Maximum value for number generation
    """
    
    def __init__(self, input_string: str, legacy_data_type: str = None):
        self.data_type = legacy_data_type
        self.input_type = None
        self.table = None
        self.column = None
        self.xpath = None
        self.jsonpath = None
        self.regexp = None
        self.template = '{{__value__}}'
        self.min = 0
        self.max = 1000000
        self.parse_and_set(input_string, legacy_data_type)
    
    def __str__(self) -> str:
        base_string = f"Selector[data_type='{self.data_type}', input_type='{self.input_type}', "
        if self.input_type == 'csv':
            base_string = base_string + f"column='{self.column}'"
        elif self.input_type == 'xml':
            base_string = base_string + f"path='{self.xpath}'"
        elif self.input_type == 'json':
            base_string = base_string + f"path='{self.jsonpath}'"
        elif self.input_type == 'db':
            base_string = base_string + f"table='{self.table}', column='{self.column}'"
        else:
            base_string = base_string + f"table='{self.table}', column='{self.column}', xpath='{self.xpath}', jsonpath='{self.jsonpath}', regexp='{self.regexp}'"
        if self.template is not None:
            base_string = base_string + f", template='{self.template}'"
        return base_string + ']'

    def parse_and_set(self, input_string: str, legacy_data_type: str = None) -> None:
        """
        Parse the input string and set selector attributes.
        
        Args:
            input_string: String to parse, either legacy format or (key=value,...)
            legacy_data_type: Legacy data type for backwards compatibility
        """
        if input_string.startswith('(') and not input_string.endswith(')'):
            print(f"Selector string is not correctly put in brackets: '{input_string}'")
            sys.exit(4)

        if input_string.startswith('(') and input_string.endswith(')'):
            input_parts = input_string[1:-1].split(',')  # remove brackets and split

            attributes = {}
            for part in input_parts:
                key, value = part.strip().split('=')
                attributes[key] = value

            self.data_type = attributes.get('type', self.data_type)
            self.table = attributes.get('table', self.table)
            self.column = attributes.get('column', self.column)
            self.xpath = attributes.get('xpath', self.xpath)
            self.jsonpath = attributes.get('jsonpath', self.jsonpath)
            self.regexp = attributes.get('regexp', self.regexp)
            self.input_type = attributes.get('input-type', self.input_type)
            self.template = attributes.get('template', self.template)
            self.min = int(attributes.get('min', self.min))
            self.max = int(attributes.get('max', self.max))

        else:
            # legacy parameter setting:
            if input_string.isnumeric():
                self.input_type = 'csv'
                self.column = input_string
            else:
                self.input_type = 'xml'
                self.xpath = input_string
