#!/usr/bin/env python3

# pip install objectrest pydantic
# python3 ./export_meshmapper_to_gpx_for_google_earth.py "repeaters.gpx"

import objectrest
from pydantic import BaseModel
import argparse

DATA_URL = "https://den.meshmapper.net/api.php?request=repeaters"
GPX_CREATOR_NAME = "MeshMapper GPX Exporter"
GPX_NAME = "MeshMapper Repeaters"
GPX_VERSION = "1.1"


class Repeater(BaseModel):
    id: str
    hex_id: str
    name: str
    lat: float
    lon: float
    last_heard: int
    created_at: str
    enabled: int
    power: str
    iata: str
    can_reach: str | None


def _download_repeaters() -> list[Repeater]:
    return objectrest.get_object(url=DATA_URL, model=Repeater, extract_list=True)

def _generate_gpx_entry(repeater: Repeater) -> str:
    return f'<wpt lat="{repeater.lat}" lon="{repeater.lon}"><name>{repeater.name}</name><desc>Power: {repeater.power}, Last Heard: {repeater.last_heard}</desc></wpt>'

def _export_to_gpx(repeaters: list[Repeater]) -> str:
    gpx = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?><gpx version="{GPX_VERSION}" creator="{GPX_CREATOR_NAME}"><metadata><name>{GPX_NAME}</name></metadata>'

    for repeater in repeaters:
        gpx += _generate_gpx_entry(repeater=repeater)

    gpx += '</gpx>'

    return gpx

def main():
    ap = argparse.ArgumentParser(description="MeshMapper Repeaters → GPX converter")
    ap.add_argument("filename", help="Output GPX filename (e.g. repeaters.gpx)")
    args = ap.parse_args()

    print("Downloading repeaters...")
    repeaters: list[Repeater] = _download_repeaters()
    gpx_content: str = _export_to_gpx(repeaters=repeaters)

    with open(args.filename, "w", encoding="utf-8") as f:
        f.write(gpx_content)


if __name__ == "__main__":
    main()
