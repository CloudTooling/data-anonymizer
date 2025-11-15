"""
Unit tests for the Source class.
"""

import pytest
from source import Source


class TestSourceCreation:
    """Test Source object creation."""
    
    def test_create_simple_source(self):
        """Test creating a simple source."""
        source = Source("data.csv")
        assert source.name == "data.csv"
        assert source.sub_source is None
    
    def test_create_source_with_subsource(self):
        """Test creating source with sub-source."""
        source = Source("database://server/db", "users_table")
        assert source.name == "database://server/db"
        assert source.sub_source == "users_table"


class TestSourceEquality:
    """Test Source equality and hashing."""
    
    def test_equal_sources_without_subsource(self):
        """Test that sources with same name are equal."""
        source1 = Source("data.csv")
        source2 = Source("data.csv")
        assert source1 == source2
    
    def test_different_names_not_equal(self):
        """Test that sources with different names are not equal."""
        source1 = Source("data1.csv")
        source2 = Source("data2.csv")
        assert source1 != source2
