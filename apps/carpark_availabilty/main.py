#!/usr/bin/env python

import logging
import sys
import requests
from config import config
import json
import pandas as pd


def read_carpark_info_from_csv():
    df = pd.read_csv("./datasets/hdb-carpark-information.csv",
                     index_col=["car_park_no"])
    return df


def fetch_carpark_availability():
    url_carpark_availability = config.get("url_carpark_availability")
    response = requests.get(url_carpark_availability)

    payload = json.loads(response.text)
    return payload


def fetch_carpark_data_for_items():
    payload = fetch_carpark_availability()
    items = payload.get("items")[0]
    if items is not None:
        carpark_data = items.get("carpark_data")
        yield from carpark_data


def enrich_carpark_info(carpark_info: dict, df):
    row = df.loc[df.index.isin([carpark_info.get("carpark_number")])]
    carpark_info["address"] = row["address"].squeeze()
    carpark_info["x_coord"] = row["x_coord"].squeeze()
    carpark_info["y_coord"] = row["y_coord"].squeeze()
    carpark_info["car_park_type"] = row["car_park_type"].squeeze()
    carpark_info["short_term_parking"] = row["short_term_parking"].squeeze()
    carpark_info["free_parking"] = row["free_parking"].squeeze()
    carpark_info["night_parking"] = row["night_parking"].squeeze()
    logging.debug("GOT %s", carpark_info)


def main():
    logging.info("START")
    df = read_carpark_info_from_csv()
    for carpark_info in fetch_carpark_data_for_items():
        enrich_carpark_info(carpark_info, df)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
