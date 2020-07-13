# Steven Wang 2020

import datetime
import requests
import time
import yaml


def watch_market(interval: int = 2):
    """"""
    with open("watch_market.yaml", "r") as f:
        conf_dict = yaml.safe_load(f)
    with open("stdout_conf.yaml", "r") as f:
        stdout_conf_dict = yaml.safe_load(f)

    field_string = ",".join(conf_dict["field_list"])
    symbol_string = ",".join(conf_dict["symbol_list"])

    snapshot_dict = {1: {x: 0 for x in conf_dict["symbol_list"]}}
    up_down_mask = {x: 0 for x in conf_dict["symbol_list"]}

    session = requests.Session()
    while True:
        resp = session.get(
            url=conf_dict["yahoo_finance_api_entry"]
            .replace("replace_field", field_string)
            .replace("replace_symbol", symbol_string)
        )
        snapshot_time = str(
            datetime.datetime.fromtimestamp(
                resp.json()["quoteResponse"]["result"][0]["regularMarketTime"]
            ).strftime("%Y%m%d %H:%M:%S")
        )
        snapshot_dict[0] = snapshot_dict[1]
        snapshot_dict[1] = {
            x["symbol"]: x["regularMarketPrice"]
            for x in resp.json()["quoteResponse"]["result"]
        }
        for _ in conf_dict["symbol_list"]:
            diff = snapshot_dict[1][_] - snapshot_dict[0][_]
            if diff > 0:
                up_down_mask[_] = 1
            elif diff < 0:
                up_down_mask[_] = -1
            else:
                up_down_mask[_] = 0
        print(
            " " * 21
            + "".join(
                "{:20}".format(
                    stdout_conf_dict["bold"] + str(x) + stdout_conf_dict["reset"]
                )
                for x in snapshot_dict[1].keys()
            )
        )
        print(
            snapshot_time
            + " " * 4
            + "".join(
                "{:20}".format(
                    stdout_conf_dict[conf_dict["color_mapping"][up_down_mask[_]]]
                    + str(x)
                    + stdout_conf_dict["reset"]
                )
                for _, x in snapshot_dict[1].items()
            )
        )

        time.sleep(interval)


if __name__ == "__main__":
    watch_market()
