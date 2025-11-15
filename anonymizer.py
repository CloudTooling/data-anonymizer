"""
Core anonymization logic for CSV Anonymizer.
Handles value anonymization with regex and template support.
"""

import re
import numbers
from typing import Dict
from jinja2 import Environment
from faker_utils import get_fake_dict


def unidecode_filter(text: str) -> str:
    """
    Simple German umlaut replacement filter.
    
    Args:
        text: Text to process
        
    Returns:
        Text with umlauts replaced
    """
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        'ß': 'ss'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def search_and_replace_dynamic(input_string: str, pattern: str, replacement: str) -> str:
    """
    Match input string against pattern and replace group(1).
    
    Args:
        input_string: String to process
        pattern: Regular expression pattern
        replacement: Replacement string
        
    Returns:
        Modified string or original if pattern doesn't match
    """
    p = re.compile(pattern)
    m = p.match(input_string)
    if m is None:
        print(f"WARN: Regexp does not match inputstring '{input_string}' - no change!")
        return input_string
    
    start_pos = m.start(1)
    return f"{input_string[:m.start(1)]}{replacement}{input_string[m.end(1):]}"


def anonymize_value(selector, original_value, context: Dict[str, str], faker, template_env: Environment):
    """
    Anonymize a single value based on selector configuration.
    
    Args:
        selector: Selector object with anonymization rules
        original_value: Original value to anonymize
        context: Context dictionary for template rendering
        faker: Faker instance
        template_env: Jinja2 environment
        
    Returns:
        Anonymized value
    """
    is_number = isinstance(original_value, numbers.Number)
    value_to_anonymize = original_value

    if not is_number and selector.regexp is not None:
        pattern = re.compile(selector.regexp)
        match = pattern.match(value_to_anonymize)
        if match is not None:
            value_to_anonymize = match.group(1)

    # empty values should stay empty:
    anonymized_value = get_fake_dict(selector, faker)[value_to_anonymize] if not None or is_number or len(original_value) > 0 else ''

    if not is_number and selector.regexp is not None:
        anonymized_value = search_and_replace_dynamic(original_value, selector.regexp, anonymized_value)

    jinja_template = template_env.from_string(selector.template)
    context['__value__'] = anonymized_value
    context['__original_value__'] = original_value
    
    if selector.column is not None:
        if selector.column.isnumeric():
            context["col_" + selector.column] = anonymized_value
        else:
            context[selector.column] = anonymized_value
    if selector.xpath is not None:
        context[selector.xpath] = anonymized_value    
    if selector.jsonpath is not None:
        context[selector.jsonpath] = anonymized_value

    # Extract values enclosed between "{{" and "}}" as new anonymization types:
    pattern = re.compile(r'\{\{(.*?)(?:\||\}\})')
    value_types = pattern.findall(selector.template)
    for value_type in value_types:
        value_type = value_type.strip()
        if not value_type.startswith('__') and not value_type.endswith('__'):
            # Create a temporary selector for the type
            from selector import Selector
            tmp_selector = Selector(f'(type={value_type})')
            context[value_type] = get_fake_dict(tmp_selector, faker)[original_value]

    return jinja_template.render(context)
