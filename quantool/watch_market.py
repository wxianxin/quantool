# Steven Wang 2020

import datetime
import requests
import pkgutil
import time
import yaml


def print_row(
    snapshot_time: str,
    stdout_conf_dict: dict,
    conf_dict: dict,
    up_down_mask: list,
    row_dict: dict,
    row_mask_list: dict,
    row_position: str,
):
    """"""
    selected_row_dict = {x: row_dict[x] for x in row_mask_list if x in row_mask_list}
    selected_up_down_mask = {
        x: up_down_mask[x] for x in row_mask_list if x in row_mask_list
    }
    print(
        snapshot_time
        + " "
        + "".join(
            "{:>18}".format(
                stdout_conf_dict[conf_dict["color_mapping"][selected_up_down_mask[_]]]
                + str(x)
                + stdout_conf_dict["reset"]
            )
            for _, x in selected_row_dict.items()
        ),
        end=row_position,
    )


def print_table(
    snapshot_time: str,
    stdout_conf_dict: dict,
    conf_dict: dict,
    up_down_mask: list,
    row_dict: dict,
):
    """"""
    for row_num in conf_dict["symbol_dict"].keys():
        print_row(
            " " * 17,
            stdout_conf_dict,
            conf_dict,
            up_down_mask,
            {x: x for x in row_dict.keys()},
            conf_dict["symbol_dict"][row_num],
            "\n",
        )
        print_row(
            snapshot_time,
            stdout_conf_dict,
            conf_dict,
            up_down_mask,
            row_dict,
            conf_dict["symbol_dict"][row_num],
            "\n",
        )


def watch_market(interval: int = 2):
    """"""

    data = pkgutil.get_data(__name__, "watch_market.yaml")
    conf_dict = yaml.safe_load(data)
    data = pkgutil.get_data(__name__, "stdout_conf.yaml")
    stdout_conf_dict = yaml.safe_load(data)

    with open("watch_market.yaml", "r") as f:
        conf_dict = yaml.safe_load(f)
    with open("stdout_conf.yaml", "r") as f:
        stdout_conf_dict = yaml.safe_load(f)

    symbol_list = []
    for row in conf_dict["symbol_dict"].values():
        symbol_list += row
    field_string = ",".join(conf_dict["field_list"])
    symbol_string = ",".join(symbol_list)

    snapshot_dict = {1: {x: 0 for x in symbol_list}}
    up_down_mask = {x: 0 for x in symbol_list}

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
        for _ in symbol_list:
            diff = snapshot_dict[1][_] - snapshot_dict[0][_]
            if diff > 0:
                up_down_mask[_] = 1
            elif diff < 0:
                up_down_mask[_] = -1
            else:
                up_down_mask[_] = 0

        print_table(
            snapshot_time, stdout_conf_dict, conf_dict, up_down_mask, snapshot_dict[1],
        )

        time.sleep(interval)


if __name__ == "__main__":
    __name__ = "quantool"
    watch_market()
