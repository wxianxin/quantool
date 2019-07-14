"""Unit test for option"""

__author__ = "Steven Wang"

import quantool

option_data = {
    "option_type": "C",
    "s": 100,
    "k": 100,
    "r": 0.05,
    "tau": 1,
    "sigma": 0.25,
    "d": 0,
    "v": 0,
}

benchmark = {
    "C_price": 12.33599893,
    "P_price": 7.45894138,
    "C_greeks": {
        "delta": 0.62740946,
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


def test_get_price():
    option = quantool.Option(**option_data)
    print(option.get_price())


def test_get_greeks():
    option = quantool.Option(**option_data)
    print(option.get_greeks())


if __name__ == "__main__":
    test_get_price()
    test_get_greeks()
