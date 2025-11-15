"""
Utility functions for CSV Anonymizer.
"""

import re


def find_rightmost_colon(input_string: str) -> int:
    """
    Find the rightmost colon that is not part of '::'.
    
    Args:
        input_string: String to search
        
    Returns:
        Position of rightmost single colon, or None if not found
    """
    # Use a negative lookbehind assertion to exclude '::'
    pattern = r'(?<!:):(?!:)'
    
    matches = re.finditer(pattern, input_string)
    positions = [match.start() for match in matches]
    
    if positions:
        return max(positions)
    else:
        return None


def print_selector_map(selector_map: dict) -> None:
    """
    Print selector map for debugging.
    
    Args:
        selector_map: Dictionary mapping sources to selectors
    """
    for key in selector_map.keys():
        selectors = selector_map[key]
        print(f"input '{key}':")
        for sel in selectors:
            print(f'  selector: {sel}')
