"""Calculate option greeks: 
    1st order:
        Delta
        Vega
        Theta
        Rho
        Lambda
        Epsilon
    2nd order:
        Gamma

"""

__author__ = "Steven Wang"

import math
import numpy as np
from scipy.stats import norm


class Option(object):
    """"""

    def __init__(
        self,
        option_type: str,
        s: float,
        k: float,
        r: float,
        tau: float,
        sigma: float = np.nan,
        v: float = np.nan,
    ):
        """"""
        self.option_type = option_type
        self.s = s
        self.k = k
        self.r = r
        self.tau = tau
        self.sigma = sigma
        self.v = v

    def get_price(self):
        """TODO test"""
        d1 = (
            math.log(self.s / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.tau
        ) / (self.sigma * self.tau)
        d2 = d1 - self.sigma * self.tau
        if self.option_type == "C":
            self.v = (
                norm.cdf(d1) * self.s
                - norm.cdf(d2) * math.e ** (-self.r * self.tau) * self.k
            )
        elif self.option_type == "P":
            self.v = (
                norm.cdf(-d2) * math.e ** (-self.r * self.tau) * self.k
                - norm.cdf(-d1) * self.s
            )
        else:
            raise Exception("Unknown option type !!!")

        return self.v

    def get_greeks(self):
        """"""
        pass

