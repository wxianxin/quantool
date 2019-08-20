"""Unit test for option"""

__author__ = "Steven Wang"

import math
import pytest

option_data = {
    "option_type": "C",
    "s": 100,
    "k": 100,
    "r": 0.05,
    "tau": 2,
    "sigma": 0.25,
    "d": 0.02,
    "v": 0,
}

benchmark = {
    "C_price": 16.0724937228103,
    "P_price": 10.477291611173932,
    "C_greeks": {
        "delta": 0.60608666,
        "vega": 37.84198319,
        "theta": -7.25049527,
        "rho": 50.40494748,
        "gamma": 0.01513679,
    },
    "P_greeks": {
        "delta": -0.37259054,
        "vega": 37.84198319,
        "theta": -2.49434815,
        "rho": -44.71799497,
        "gamma": 0.01513679,
    },
}


def test_get_price(generate_option):
    """"""
    option = generate_option
    assert option.get_price() == benchmark["C_price"]
    option.option_type = "P"
    assert option.get_price() == benchmark["P_price"]


def test_get_greeks(generate_option):
    """TODO"""
    option = generate_option
    print(option.get_greeks())


def test_get_iv(generate_option):
    """"""
    option = generate_option
    option = generate_option
    math.isclose(option.get_iv(16.0724937228103).x, 0.25)


if __name__ == "__main__":
    pytest.main(["-v", "-s", "-r", "p,f,E", "-p", "no:warnings"])
# pytest -v -s -r p,f,E -p no:warnings .
