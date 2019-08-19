"""conftest.py for quantool unit tests
"""

import pytest
import quantool

option_data_dict = {
    "option_type": "C",
    "s": 100,
    "k": 100,
    "r": 0.05,
    "tau": 2,
    "sigma": 0.25,
    "d": 0.02,
    "v": 0,
}


@pytest.fixture
def generate_option_data_dict():
    return option_data_dict


@pytest.fixture
def generate_option(option_data_dict=option_data_dict):
    """prepare option object"""
    option = quantool.Option(**option_data_dict)
    return option
