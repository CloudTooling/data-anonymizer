"""
Unit tests for core anonymization logic.
"""

import pytest
from faker import Factory
from jinja2 import Environment


from anonymizer import unidecode_filter, search_and_replace_dynamic, anonymize_value
from selector import Selector


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


class TestUnidecodeFilter:
    """Test the unidecode filter."""

    def test_replace_german_umlauts_lowercase(self):
        """Test replacing lowercase German umlauts."""
        assert unidecode_filter("äöü") == "aeoeue"

    def test_replace_german_umlauts_uppercase(self):
        """Test replacing uppercase German umlauts."""
        assert unidecode_filter("ÄÖÜ") == "AeOeUe"

    def test_replace_eszett(self):
        """Test replacing ß."""
        assert unidecode_filter("Straße") == "Strasse"


class TestAnonymizeValue:
    """Test the core anonymize_value function."""

    def test_anonymize_simple_string(self, faker, template_env):
        """Test anonymizing a simple string value."""
        selector = Selector("(type=first_name,column=0)")
        result = anonymize_value(selector, "John", {}, faker, template_env)

        assert isinstance(result, str)
        assert result != "John"
        assert len(result) > 0
