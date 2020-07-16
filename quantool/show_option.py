"""
Get option data
"""

__author__ = "Steven Wang"


from . import query_yahoo
from .option import Option


def prepare_option(symbol_string: str, r: float = None):
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

    return option_dict


def show_option(symbol_string: str):
    """"""
    snapshot_time, r_snapshot_dict = query_yahoo.get_equity(
        "regularMarketTime,regularMarketPrice", "^TNX"
    )
    r = r_snapshot_dict["^TNX"]
    option_dict = prepare_option(symbol_string, r)
    for _ in option_dict.keys():
        print(f"{_} options:")
        for x in option_dict[_]:
            calculated_price = x.get_price()
            calculated_iv = x.get_iv(calculated_price)["x"] ** 2
            print(
                "    K: {} | P: {:9.4f} | IV: {:9.4f}".format(
                    x.k, calculated_price, calculated_iv
                )
            )


if __name__ == "__main__":
    pass
