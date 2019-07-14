"""Calculate option greeks:

1st order:
    - Delta
    - Vega
    - Theta
    - Rho
    - Epsilon

2nd order:
    - Gamma

"""

__author__ = "Steven Wang"

import math
import numpy as np
from scipy.stats import norm


class Option(object):
    """
    NOTE: All numeric values are with unit 1; No percent or any convention is used.
    NOTE: For now the code is structured for readability not for performance. 
            A performance-oriented c++ implementation maybe created later.
    """

    def __init__(
        self,
        option_type: str,
        s: float,
        k: float,
        r: float,
        tau: float,
        sigma: float = np.nan,
        d: float = 0,
        v: float = np.nan,
    ):
        """"""
        self.option_type = option_type
        self.s = s
        self.k = k
        self.r = r
        self.tau = tau
        self.sigma = sigma
        self.d = d
        self.v = v
        self.greek_dict = {}

    def get_price(self):
        """Get option price"""
        d1 = (
            math.log(self.s / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.tau
        ) / (self.sigma * self.tau)
        d2 = d1 - self.sigma * self.tau
        if self.option_type == "C":
            self.v = (
                norm.cdf(d1) * self.s
                - norm.cdf(d2) * math.exp(-self.r * self.tau) * self.k
            )
        elif self.option_type == "P":
            self.v = (
                norm.cdf(-d2) * math.exp(-self.r * self.tau) * self.k
                - norm.cdf(-d1) * self.s
            )
        else:
            raise Exception("Unknown option type !!!")

        return self.v

    def get_greeks(self):
        """Calculate the greeks"""
        d1 = (
            math.log(self.s / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.tau
        ) / (self.sigma * self.tau)
        d2 = d1 - self.sigma * self.tau
        if self.option_type == "C":
            self.greek_dict["delta"] = math.exp(-self.d * self.tau) * norm.cdf(d1)
            self.greek_dict["vega"] = (
                self.k * math.exp(-self.r * self.tau) * norm.pdf(d2) * self.tau ** 0.5
            )
            self.greek_dict["theta"] = (
                -math.exp(-self.d * self.tau)
                * self.s
                * norm.pdf(d1)
                * self.sigma
                / (2 * self.tau ** 0.5)
                - self.r * self.k * math.exp(-self.r * self.tau) * norm.cdf(d2)
                + self.d * self.s * math.exp(-self.d * self.tau) * norm.cdf(d1)
            )
            self.greek_dict["rho"] = (
                self.k * self.tau * math.exp(-self.r * self.tau) * norm.cdf(d2)
            )
            self.greek_dict["gamma"] = (
                self.k
                * math.exp(-self.r * self.tau)
                * norm.pdf(d2)
                / (self.s ** 2 * self.sigma * self.tau ** 0.5)
            )

        elif self.option_type == "P":
            self.greek_dict["delta"] = -math.exp(-self.d * self.tau) * norm.cdf(-d1)
            self.greek_dict["vega"] = (
                self.k * math.exp(-self.r * self.tau) * norm.pdf(d2) * self.tau ** 0.5
            )
            self.greek_dict["theta"] = (
                -math.exp(-self.d * self.tau)
                * self.s
                * norm.pdf(d1)
                * self.sigma
                / (2 * self.tau ** 0.5)
                + self.r * self.k * math.exp(-self.r * self.tau) * norm.cdf(-d2)
                - self.d * self.s * math.exp(-self.d * self.tau) * norm.cdf(-d1)
            )
            self.greek_dict["rho"] = (
                -self.k * self.tau * math.exp(-self.r * self.tau) * norm.cdf(-d2)
            )
            self.greek_dict["gamma"] = (
                self.k
                * math.exp(-self.r * self.tau)
                * norm.pdf(d2)
                / (self.s ** 2 * self.sigma * self.tau ** 0.5)
            )

        return self.greek_dict


if __name__ == "__main__":
    pass
