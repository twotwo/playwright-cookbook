import json
import os

import pytest


try:
    from matplotlib import pyplot as plt
except Exception:
    pytestmark = pytest.mark.skip(reason="Failed to import numpy")


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


city = "beijing"


@pytest.mark.skipif(not file_exists(f"/tmp/weather-{city}.json"), reason="file not exists")
def test_render_temprature_info():
    with open(f"/tmp/weather-{city}.json", encoding="utf-8") as f:
        data = json.load(f)

    fig = plt.figure(1)
    # 绘制折线图
    fig, ax = plt.subplots(layout="constrained")

    for year, array in data["infos"].items():
        if len(array[0]) < 5:
            continue
        if year < "2015":
            continue
        # ax.plot(array[0], [int(num) for num in array[1]], label=year)
        ax.plot(array[0], [int(num) for num in array[2]], label=year)
        # if year == "2015":
        #     break

    ax.set_title(f"Over years of {city.capitalize()}")
    ax.set_xlabel("March days for high temp")
    ax.set_ylabel("Temprature(°C)")
    ax.legend()
    plt.savefig(f"weather-{city}.png", dpi=fig.dpi)
