import json
import os

import pytest


def file_exists(file_path):
    return os.path.exists(file_path)


@pytest.mark.skipif(not file_exists("/tmp/weather-beijing.json"), reason="file not exists")
def test_read_temprature_info():
    with open("/tmp/weather-beijing.json", encoding="utf-8") as f:
        data = json.load(f)

    info_2011 = data["infos"]["2011"]
    print("axis low high")
    for axis, low, high in zip(info_2011[0], info_2011[1], info_2011[2]):
        print(axis, low, high)
