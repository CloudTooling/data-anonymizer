"""
Faker utilities for CSV Anonymizer.
Handles creation and management of faker dictionaries.
"""

import random
from collections import defaultdict
from typing import Dict, Callable
from faker import Factory


FAKER_DICTS: Dict[str, defaultdict] = {}


def get_random_int(start: int = 0, end: int = 1000000) -> Callable[[], int]:
    """Generate a random integer function."""
    return lambda: random.randint(start, end)


def dummy_value() -> str:
    """Return a dummy value."""
    return 'dummy'


def create_faker_dict(selector, faker) -> defaultdict:
    """
    Create a faker dictionary for the given data type.
    
    Args:
        selector: Selector object with data_type and range parameters
        faker: Faker instance
        
    Returns:
        A defaultdict that generates fake values for keys
    """
    fake_dict = None
    data_type = selector.data_type
    
    if data_type == 'name':
        fake_dict = defaultdict(faker.name)
    elif data_type == 'first_name':
        fake_dict = defaultdict(faker.first_name)
    elif data_type == 'last_name':
        fake_dict = defaultdict(faker.last_name)
    elif data_type == 'number':
        fake_dict = defaultdict(get_random_int(selector.min, selector.max))
    elif data_type == 'url':
        fake_dict = defaultdict(faker.url)
    elif data_type == 'email':
        fake_dict = defaultdict(faker.email)
    elif data_type == 'phone_number':
        fake_dict = defaultdict(faker.phone_number)
    elif data_type == 'address':
        fake_dict = defaultdict(faker.address)
    elif data_type == 'zip' or data_type == 'postcode':
        fake_dict = defaultdict(faker.postcode)
    elif data_type == 'city':
        fake_dict = defaultdict(faker.city)
    elif data_type == 'city_suffix':
        fake_dict = defaultdict(faker.city_suffix)
    elif data_type == 'street' or data_type == 'street_address':
        fake_dict = defaultdict(faker.street_address)
    elif data_type == 'street_name':
        fake_dict = defaultdict(faker.street_name)
    elif data_type == 'iban':
        fake_dict = defaultdict(faker.iban)
    elif data_type == 'sentence':
        fake_dict = defaultdict(faker.sentence)
    elif data_type == 'word':
        fake_dict = defaultdict(faker.word)
    elif data_type == 'text':
        fake_dict = defaultdict(faker.text)
    elif data_type == 'date':
        fake_dict = defaultdict(faker.date)
    elif data_type == 'uuid4':
        fake_dict = defaultdict(faker.uuid4)
    elif data_type == 'passport_number':
        fake_dict = defaultdict(faker.passport_number)
    elif data_type == 'company':
        fake_dict = defaultdict(faker.company)
    elif data_type == 'dummy':
        fake_dict = defaultdict(dummy_value)

    return fake_dict


def get_fake_dict(selector, faker) -> defaultdict:
    """
    Get or create a faker dictionary for the selector.
    
    Args:
        selector: Selector object
        faker: Faker instance
        
    Returns:
        A faker dictionary for the selector's data type
    """
    global FAKER_DICTS

    fake_dict = FAKER_DICTS.get(selector.data_type, None)
    if fake_dict is None:
        fake_dict = create_faker_dict(selector, faker)
        FAKER_DICTS[selector.data_type] = fake_dict
    return fake_dict
