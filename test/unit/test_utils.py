"""
Unit tests for utility functions.
"""

import pytest
from utils import find_rightmost_colon, print_selector_map
from source import Source
from selector import Selector


class TestFindRightmostColon:
    """Test the find_rightmost_colon function."""
    
    def test_single_colon(self):
        """Test finding single colon."""
        result = find_rightmost_colon("file.csv:0")
        assert result == 8
    
    def test_multiple_colons(self):
        """Test finding rightmost of multiple colons."""
        result = find_rightmost_colon("a:b:c:d")
        assert result == 5
    
    def test_double_colon_ignored(self):
        """Test that double colons are ignored."""
        result = find_rightmost_colon("namespace::element:selector")
        assert result == 18
    
    def test_no_colon(self):
        """Test string without colon."""
        result = find_rightmost_colon("file.csv")
        assert result is None
