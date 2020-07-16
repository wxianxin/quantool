"""
"""

__author__ = "Steven Wang"

import datetime
import requests

_equity_api_entry = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&fields=replace_field&symbols=replace_symbol"
_option_api_entry = "https://query2.finance.yahoo.com/v7/finance/options/replace_symbol"


def get_equity(
    field_string: str, symbol_string: str, requests_session: requests.Session = None
):
    """"""
    if requests_session is None:
        session = requests.Session()
    else:
        session = requests_session
    resp = session.get(
        url=_equity_api_entry.replace("replace_field", field_string).replace(
            "replace_symbol", symbol_string
        )
    )
    snapshot_time = str(
        datetime.datetime.fromtimestamp(
            resp.json()["quoteResponse"]["result"][0]["regularMarketTime"]
        ).strftime("%Y%m%d %H:%M:%S")
    )
    snapshot_dict = {
        x["symbol"]: x["regularMarketPrice"]
        for x in resp.json()["quoteResponse"]["result"]
    }

    return snapshot_time, snapshot_dict


def get_option(symbol_string: str):
    """"""
    session = requests.Session()
    resp = session.get(url=_option_api_entry.replace("replace_symbol", symbol_string))
    snapshot_dict = resp.json()
    return snapshot_dict


if __name__ == "__main__":
    print(get_option("AMD"))
