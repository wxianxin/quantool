import requests
import json
import urllib3

# Ignore insecure error messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def acctPos(acct_id: str):

    base_url = "https://192.168.8.9:5001/v1/api/"

    # account management
    endpoint = {
        "summary": f"portfolio/{acct_id}/summary",
        "position": f"portfolio/{acct_id}/positions/0",  # 0 is the page number
        "position_id": f"portfolio/{acct_id}/position/_replace_contract_id_",
    }
    pos_req = requests.get(url=base_url + endpoint["summary"], verify=False)
    print(pos_req.status_code)

    return pos_req.json()


def get_market():
    base_url = "https://192.168.8.9:5001/v1/api/"
    # market data
    # To get field id: https://interactivebrokers.github.io/cpwebapi/endpoints
    # Note option data can be slow to load as IBKR may be calculating it on the fly; it may take up to 1 minute
    field_dict = {
        "base": {
            "last_price": 31,
            "symbol": 55,
            "bid_price": 84,
            "bid_size": 88,
            "ask_price": 86,
            "ask_size": 85,
        },
        "security": {
            "shortable_shares": 7636,
            "fee_rate": 7637,
            "ema_200": 7674,
            "ema_100": 7675,
            "ema_50": 7676,
            "ema_20": 7677,
        },
        "option": {
            "implied_vol": 7084,
            "put_call_interest": 7085,
            "delta": 7308,
            "gamma": 7309,
            "theta": 7310,
            "vega": 7607,
            "impl_vol": 7633,
        },
        "bond": {},
    }

    endpoint = "iserver/marketdata/snapshot"
    conid = "conids=265598,8314"  # AAPL, IBM
    fields = "fields=31,55,84,86"
    params = "&".join([conid, fields])
    request_url = "".join([base_url, endpoint, "?", params])
    md_req = requests.get(url=request_url, verify=False)
    md_json = json.dumps(md_req.json(), indent=2)
    print(md_req)
    print(md_json)

    return None


def get_hist():
    base_url = "https://192.168.8.9:5001/v1/api/"
    # historical data
    # only single conid allowed at a time
    endpoint = "hmds/history"
    conid = "conid=4391"
    period = "period=1w"
    bar = "bar=1d"
    outsideRth = "outsideRth=true"  # optional
    barType = "barType=midpoint"  # optional
    params = "&".join(
        [
            conid,
            period,
            bar,
            outsideRth,
            barType,
        ]
    )
    request_url = "".join([base_url, endpoint, "?", params])
    hd_req = requests.get(url=request_url, verify=False)
    hd_json = json.dumps(hd_req.json(), indent=2)
    print(hd_req)
    print(hd_json)

    return None


def get_contract():
    # contract search (e.g. AAPL is 265598)
    base_url = "https://192.168.8.9:5001/v1/api/"
    endpoint = "iserver/secdef/search"
    json_body = {"symbol": "amd", "secType": "STK", "name": False}
    contract_req = requests.post(url=base_url + endpoint, verify=False, json=json_body)
    print(contract_req.json())

    # # contract info
    # endpoint = "iserver/secdef/info"
    # conid = "conid=11004968"
    # secType = "secType=FOP"
    # month = "month=JUL23"
    # exchange = "exchange=CME"
    # strike = "strike=4800"  # remove these 2 for more data
    # right = "right=C"  # remove these 2 for more data
    # params = "&".join([conid, secType, month, exchange, strike, right])
    # request_url = "".join([base_url, endpoint, "?", params])
    # contract_req = requests.get(url=request_url, verify=False)
    # contract_json = json.dumps(contract_req.json(), indent=2)
    # print(contract_req)
    # print(contract_json)

    # # contract strike
    # endpoint = "iserver/secdef/strikes"
    # conid = "conid=11004968"
    # secType = "secType=FOP"
    # month = "month=JUL23"
    # exchange = "exchange=CME"
    # params = "&".join([conid, secType, month, exchange])
    # request_url = "".join([base_url, endpoint, "?", params])
    # strikes_req = requests.get(url=request_url, verify=False)
    # strikes_json = json.dumps(strikes_req.json(), indent=2)
    # print(strikes_req)
    # print(strikes_json)

    return contract_req


def place_order(acct_id: str):

    base_url = "https://localhost:5000/v1/api/"
    endpoint = f"iserver/account/{acct_id}/orders"

    json_body = {
        "orders": [
            {
                "conid": 265598,
                "orderType": "MKT",
                "side": "BUY",
                "tif": "DAY",
                "quantity": 10,
            }
        ]
    }

    json_body = {
        "orders": [
            {
                "conid": 265598,
                "orderType": "LMT",
                "price": 185,
                "side": "SELL",
                "tif": "DAY",
                "quantity": 10,
            }
        ]
    }

    json_body = {
        "orders": [
            {
                "conid": 265598,
                "orderType": "STP",
                "price": 185,
                "side": "SELL",
                "tif": "DAY",
                "quantity": 10,
            }
        ]
    }
    order_req = requests.post(url=base_url + endpoint, verify=False, json=json_body)
    order_json = json.dumps(order_req.json(), indent=2)

    print(order_req.status_code)
    print(order_json)


def reply_order():
    """Reply when a confirmation is needed for an order"""
    base_url = "https://localhost:5000/v1/api/"
    endpoint = "iserver/reply/"
    replyId = "7a45bf17-ae07-430f-9888-a4d79539aaa0"
    reply_url = "".join([base_url, endpoint, replyId])
    json_body = {"confirmed": True}
    order_req = requests.post(url=reply_url, verify=False, json=json_body)
    order_json = json.dumps(order_req.json(), indent=2)
    print(order_req.status_code)
    print(order_json)


def query_order():

    base_url = "https://localhost:5000/v1/api/"
    endpoint = "iserver/account/orders"

    order_req = requests.get(url=base_url + endpoint, verify=False)
    order_json = json.dumps(order_req.json(), indent=2)
    print(order_req.status_code)
    print(order_json)


def modify_order(acct_id: str):

    base_url = "https://localhost:5000/v1/api/"
    endpoint = f"iserver/account/{acct_id}/order/"
    order_id = "1010551026"
    modify_url = "".join([base_url, endpoint, order_id])

    json_body = {
        "conid": 265598,
        "orderType": "STP",
        "price": 187,
        "side": "SELL",
        "tif": "DAY",
        "quantity": 10,
    }
    order_req = requests.post(url=modify_url, verify=False, json=json_body)
    order_json = json.dumps(order_req.json(), indent=2)
    print(order_req.status_code)
    print(order_json)


def cancel_order(acct_id: str):
    base_url = "https://localhost:5000/v1/api/"
    endpoint = f"iserver/account/{acct_id}/order/"
    order_id = "1010551026"
    cancel_url = "".join([base_url, endpoint, order_id])

    cancel_req = requests.delete(url=cancel_url, verify=False)
    cancel_json = json.dumps(cancel_req.json(), indent=2)
    print(cancel_req.status_code)
    print(cancel_json)


if __name__ == "__main__":
    # data = acctPos("DU2534309")
    # data = get_market()
    data = get_hist()
    # data = historicalData()
    # data = get_contract()
    print(data)
