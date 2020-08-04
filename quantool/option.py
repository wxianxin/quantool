"""Option Class

Calculate Black Scholes Price

Get Black Scholes Implied Volatitlity

Greeks:
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
from scipy import optimize
from scipy.stats import norm


class Option(object):
    """
    NOTE: All numeric values are with the unit of 1, which means no percent nor any
            convention is used.
    NOTE: For now the code is structured for readability rather than performance.
            A performance-oriented c++ implementation may be created later.
    """

    _notation_dict = {
        "C": "European Call Option",
        "P": "European Put Option",
        "c": "American Call Option",
        "p": "American Put Option",
    }

    def __init__(
        self,
        option_type: str,
        S: float,
        K: float,
        r: float,
        tau: float,
        sigma: float = None,
        d: float = 0,
        v: float = None,
    ):
        """"""
        self.option_type = option_type
        self.S = S
        self.K = K
        self.r = r
        self.tau = tau
        self.sigma = sigma
        self.d = d
        self.v = v
        self.greek_dict = {}

    def __repr__(self):
        """representation"""
        return (
            f"{self.option_type}, S: {self.S}, K: {self.K}, r: {self.r}, Tau:"
            f" {self.tau}, Sigma: {self.sigma}, d: {self.d}, V: {self.v}"
        )

    def __str__(self):
        """string representation"""
        return f"""{self._notation_dict[self.option_type]}
    Underlying Price: {self.S}
    Strike Price: {self.K}
    Interest Rate: {self.r}
    Time to Maturity: {self.tau}
    Underlying Standard Deviation: {self.sigma}
    Dividend Rate: {self.d}
    Option Value: {self.v}"""

    def get_price(self):
        """Get option price"""
        d1 = (
            math.log(self.S / self.K)
            + (self.r - self.d + 0.5 * self.sigma ** 2) * self.tau
        ) / (self.sigma * self.tau ** 0.5)
        d2 = d1 - self.sigma * self.tau ** 0.5
        if self.option_type == "C":
            self.v = (
                norm.cdf(d1) * math.exp(-self.d * self.tau) * self.S
                - norm.cdf(d2) * math.exp(-self.r * self.tau) * self.K
            )
        elif self.option_type == "P":
            self.v = (
                norm.cdf(-d2) * math.exp(-self.r * self.tau) * self.K
                - norm.cdf(-d1) * math.exp(-self.d * self.tau) * self.S
            )
        else:
            raise Exception("Unknown option type !!!")

        return self.v

    def get_greeks(self):
        """Calculate the greeks"""
        d1 = (
            math.log(self.S / self.K)
            + (self.r - self.d + 0.5 * self.sigma ** 2) * self.tau
        ) / (self.sigma * self.tau ** 0.5)
        d2 = d1 - self.sigma * self.tau ** 0.5
        if self.option_type == "C":
            # European Call Option
            self.greek_dict["delta"] = math.exp(-self.d * self.tau) * norm.cdf(d1)
            self.greek_dict["gamma"] = (
                self.K
                * math.exp(-self.r * self.tau)
                * norm.pdf(d2)
                / (self.S ** 2 * self.sigma * self.tau ** 0.5)
            )
            self.greek_dict["vega"] = (
                self.K * math.exp(-self.r * self.tau) * norm.pdf(d2) * self.tau ** 0.5
            )
            # self.greek_dict["vega"] = (
            #     self.S * math.exp(-self.d * self.tau) * norm.pdf(d1) * self.tau ** 0.5
            # )
            self.greek_dict["theta"] = (
                -math.exp(-self.d * self.tau)
                * self.S
                * norm.pdf(d1)
                * self.sigma
                / (2 * self.tau ** 0.5)
                - self.r * self.K * math.exp(-self.r * self.tau) * norm.cdf(d2)
                + self.d * self.S * math.exp(-self.d * self.tau) * norm.cdf(d1)
            )
            self.greek_dict["rho"] = (
                self.K * self.tau * math.exp(-self.r * self.tau) * norm.cdf(d2)
            )

        elif self.option_type == "P":
            # European Put Option
            self.greek_dict["delta"] = -math.exp(-self.d * self.tau) * norm.cdf(-d1)
            self.greek_dict["gamma"] = (
                self.K
                * math.exp(-self.r * self.tau)
                * norm.pdf(d2)
                / (self.S ** 2 * self.sigma * self.tau ** 0.5)
            )
            self.greek_dict["vega"] = (
                self.K * math.exp(-self.r * self.tau) * norm.pdf(d2) * self.tau ** 0.5
            )
            self.greek_dict["theta"] = (
                -math.exp(-self.d * self.tau)
                * self.S
                * norm.pdf(d1)
                * self.sigma
                / (2 * self.tau ** 0.5)
                + self.r * self.K * math.exp(-self.r * self.tau) * norm.cdf(-d2)
                - self.d * self.S * math.exp(-self.d * self.tau) * norm.cdf(-d1)
            )
            self.greek_dict["rho"] = (
                -self.K * self.tau * math.exp(-self.r * self.tau) * norm.cdf(-d2)
            )

        return self.greek_dict

    def get_iv(self, price):
        """Get BS Implied Volatility"""

        def objective_func(sigma, price):
            """Objective function used for optimization in getting Implied Volatility."""
            self.sigma = sigma
            return (price - self.get_price()) ** 2

        # brent is the better method for unimodal function
        res = optimize.minimize_scalar(
            objective_func, bracket=(0.001, 1), args=(price), method="brent"
        )

        return res


if __name__ == "__main__":
    pass
