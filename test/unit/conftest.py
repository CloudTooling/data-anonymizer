"""
Pytest configuration and shared fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path so modules can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(autouse=True)
def reset_faker_cache():
    """Reset faker cache before each test."""
    import faker_utils
    faker_utils.FAKER_DICTS.clear()
    yield
    faker_utils.FAKER_DICTS.clear()


@pytest.fixture
def sample_csv_data():
    """Provide sample CSV data for tests."""
    return [
        ['John', 'Doe', 'john@example.com', '12345'],
        ['Jane', 'Smith', 'jane@example.com', '67890'],
        ['Bob', 'Johnson', 'bob@example.com', '11111']
    ]


@pytest.fixture
def sample_xml_data():
    """Provide sample XML data for tests."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<people>
    <person>
        <firstname>John</firstname>
        <lastname>Doe</lastname>
        <email>john@example.com</email>
    </person>
    <person>
        <firstname>Jane</firstname>
        <lastname>Smith</lastname>
        <email>jane@example.com</email>
    </person>
</people>"""


@pytest.fixture
def sample_json_data():
    """Provide sample JSON data for tests."""
    return {
        "users": [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "address": {
                    "city": "Berlin",
                    "zip": "10115"
                }
            },
            {
                "name": "Jane Smith",
                "email": "jane@example.com",
                "address": {
                    "city": "Munich",
                    "zip": "80331"
                }
            }
        ]
    }
