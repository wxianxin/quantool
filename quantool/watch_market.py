"""
"""

__author__ = "Steven Wang"

import datetime
import requests
import pkgutil
import time
import yaml

from . import query_yahoo


def print_row(
    snapshot_time: str,
    stdout_conf_dict: dict,
    conf_dict: dict,
    up_down_mask: list,
    row_dict: dict,
    row_mask_list: dict,
    row_position: int,
    row_count: int,
    style: str,
):
    """
    NOTE: python format padding also takes ANSII escape characters into account
    """
    selected_row_dict = {x: row_dict[x] for x in row_mask_list if x in row_mask_list}
    selected_up_down_mask = {
        x: up_down_mask[x] for x in row_mask_list if x in row_mask_list
    }

    if row_position == 1:
        print(
            f"{stdout_conf_dict['line_start']}{row_count + 2}A{(' ' + snapshot_time + ' ').center(90, '#')}"
        )
    snapshot_time = " " * 17
    print(
        stdout_conf_dict["line_clear"]
        + "".join(
            "{:>23}".format(
                style
                + stdout_conf_dict[conf_dict["color_mapping"][selected_up_down_mask[_]]]
                + str(x)
                + stdout_conf_dict["reset"]
            )
            for _, x in selected_row_dict.items()
        ),
        end="\n",
    )


def print_table(
    snapshot_time: str,
    stdout_conf_dict: dict,
    conf_dict: dict,
    up_down_mask: list,
    row_dict: dict,
    row_count: int,
):
    """"""
    for row_num in conf_dict["symbol_dict"].keys():
        row_int = int(row_num.replace("row_", ""))
        print_row(
            snapshot_time,
            stdout_conf_dict,
            conf_dict,
            up_down_mask,
            {x: x for x in row_dict.keys()},
            conf_dict["symbol_dict"][row_num],
            row_int * 2 - 1,
            row_count,
            stdout_conf_dict["bold"],
        )
        print_row(
            snapshot_time,
            stdout_conf_dict,
            conf_dict,
            up_down_mask,
            row_dict,
            conf_dict["symbol_dict"][row_num],
            row_int * 2,
            row_count,
            stdout_conf_dict["reset"],
        )
    print("#" * 90)


def watch_market(interval: int = 2):
    """"""

    data = pkgutil.get_data(__name__, "watch_market.yaml")
    conf_dict = yaml.safe_load(data)
    data = pkgutil.get_data(__name__, "stdout_conf.yaml")
    stdout_conf_dict = yaml.safe_load(data)

    row_count = int(list(conf_dict["symbol_dict"].keys())[-1].replace("row_", "")) * 2
    print(" Watch Market ".center(90, "#"), "\n" * (row_count + 1))

    symbol_list = []
    for row in conf_dict["symbol_dict"].values():
        symbol_list += row
    field_string = ",".join(conf_dict["field_list"])
    symbol_string = ",".join(symbol_list)

    snapshot_dict = {1: {x: 0 for x in symbol_list}}
    up_down_mask = {x: 0 for x in symbol_list}

    # for network efficiency
    session = requests.Session()
    while True:
        snapshot_time, equity_snapshot_dict = query_yahoo.get_equity(
            field_string, symbol_string, session
        )
        snapshot_dict[0] = snapshot_dict[1]
        snapshot_dict[1] = equity_snapshot_dict
        try:
            for _ in symbol_list:
                diff = snapshot_dict[1][_] - snapshot_dict[0][_]
                if diff > 0:
                    up_down_mask[_] = 1
                elif diff < 0:
                    up_down_mask[_] = -1
                else:
                    up_down_mask[_] = 0
        except KeyError:
            print(
                stdout_conf_dict["line_start"]
                + "1A"
                + stdout_conf_dict["line_clear"]
                + "!!! Yahoo API fetch fail !!!"
            )

        print_table(
            snapshot_time,
            stdout_conf_dict,
            conf_dict,
            up_down_mask,
            snapshot_dict[1],
            row_count,
        )

        time.sleep(interval)


if __name__ == "__main__":
    __name__ = "quantool"
    watch_market()
