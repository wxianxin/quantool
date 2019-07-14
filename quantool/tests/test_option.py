"""Unit test for option"""

__author__ = "Steven Wang"

import quantool

option_data = {
    "option_type": "P",
    "s": 100,
    "k": 100,
    "r": 0.05,
    "tau": 1,
    "sigma": 0.25,
    "v": 0,
}


def test_get_price():
    option = quantool.option.Option(**option_data)
    print(option.get_price())


if __name__ == "__main__":
    test_get_price()