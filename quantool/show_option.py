"""
Get option data
"""

__author__ = "Steven Wang"


from . import query_yahoo
from .option import Option


def show_option(symbol_string: str, r: float = None):
    """"""
    option_snapshot_dict = query_yahoo.get_option(symbol_string)
    option_chain_dict = option_snapshot_dict["optionChain"]["result"][0]["options"][0]
    if r is None:
        raise Exception("TODO: add default value fetch for risk-free rate")
    underlying_price = option_snapshot_dict["optionChain"]["result"][0]["quote"][
        "regularMarketPrice"
    ]
    option_dict = {"call": [], "put": []}
    for _ in option_dict.keys():
        for x in option_chain_dict[_ + "s"]:
            option_dict[_].append(
                Option(
                    option_type=_[0].upper(),
                    s=underlying_price,
                    r=r,
                    k=x["strike"],
                    tau=(x["expiration"] - x["lastTradeDate"]) / 86400 / 360,
                    sigma=x["impliedVolatility"] ** 0.5,
                )
            )



    breakpoint()
    return option_dict


if __name__ == "__main__":
    pass
