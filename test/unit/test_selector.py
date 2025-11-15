"""
Unit tests for the Selector class.
"""

import pytest
from selector import Selector


class TestSelectorParsing:
    """Test selector parsing functionality."""
    
    def test_legacy_numeric_column(self):
        """Test legacy format with numeric column."""
        selector = Selector("3", "name")
        assert selector.input_type == 'csv'
        assert selector.column == "3"
        assert selector.data_type == "name"
    
    def test_legacy_xpath(self):
        """Test legacy format with xpath."""
        selector = Selector("./person/name", "last_name")
        assert selector.input_type == 'xml'
        assert selector.xpath == "./person/name"
        assert selector.data_type == "last_name"
    
    def test_modern_format_csv(self):
        """Test modern format for CSV."""
        selector = Selector("(type=email,column=5)")
        assert selector.input_type is None
        assert selector.column == "5"
        assert selector.data_type == "email"
    
    def test_modern_format_xml(self):
        """Test modern format for XML."""
        selector = Selector("(type=name,xpath=./person/name)")
        assert selector.xpath == "./person/name"
        assert selector.data_type == "name"
    
    def test_template_parameter(self):
        """Test template parameter."""
        selector = Selector("(type=name,column=1,template={{first_name}} {{last_name}})")
        assert selector.template == "{{first_name}} {{last_name}}"
    
    def test_min_max_parameters(self):
        """Test min and max parameters for numbers."""
        selector = Selector("(type=number,column=0,min=1000,max=9999)")
        assert selector.min == 1000
        assert selector.max == 9999
