"""
Unit tests for faker utilities.
"""

import pytest
from faker import Factory
from faker_utils import get_random_int, dummy_value, create_faker_dict
from selector import Selector


@pytest.fixture
def faker():
    """Provide a faker instance."""
    return Factory.create('de_DE')


class TestRandomIntGenerator:
    """Test random integer generator."""
    
    def test_get_random_int_default_range(self):
        """Test random int with default range."""
        func = get_random_int()
        value = func()
        assert 0 <= value <= 1000000
    
    def test_get_random_int_custom_range(self):
        """Test random int with custom range."""
        func = get_random_int(100, 200)
        for _ in range(10):
            value = func()
            assert 100 <= value <= 200


class TestCreateFakerDict:
    """Test faker dictionary creation."""
    
    def test_create_name_dict(self, faker):
        """Test creating name faker dict."""
        selector = Selector("(type=name,column=0)")
        fake_dict = create_faker_dict(selector, faker)
        
        assert fake_dict is not None
        name = fake_dict["any_key"]
        assert isinstance(name, str)
        assert len(name) > 0
    
    def test_create_email_dict(self, faker):
        """Test creating email faker dict."""
        selector = Selector("(type=email,column=0)")
        fake_dict = create_faker_dict(selector, faker)
        
        email = fake_dict["key"]
        assert isinstance(email, str)
        assert '@' in email
