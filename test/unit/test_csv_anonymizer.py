"""
Unit tests for CSV anonymization.
"""

import pytest
import tempfile
import os
from faker import Factory
from jinja2 import Environment
from csv_anonymizer import anonymize_rows, anonymize_csv
from selector import Selector
from anonymizer import unidecode_filter


@pytest.fixture
def faker():
    """Provide a faker instance."""
    return Factory.create('de_DE')


@pytest.fixture
def template_env():
    """Provide a Jinja2 environment."""
    env = Environment()
    env.filters['unidecode'] = unidecode_filter
    return env


class TestAnonymizeRows:
    """Test the anonymize_rows function."""
    
    def test_anonymize_single_column(self, faker, template_env):
        """Test anonymizing a single column."""
        rows = [
            ['John', 'Doe', 'john@example.com'],
            ['Jane', 'Smith', 'jane@example.com']
        ]
        selector = Selector("(type=email,column=2)")
        
        result = list(anonymize_rows(rows, [selector], faker, template_env))
        
        assert len(result) == 2
        assert result[0][0] == 'John'
        assert result[0][1] == 'Doe'
        assert result[0][2] != 'john@example.com'
        assert '@' in result[0][2]
