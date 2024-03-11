import json
import os

import pytest


try:
    import numpy as np
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


@pytest.mark.skipif(not file_exists("/tmp/weather-beijing.json"), reason="file not exists")
def test_render_temprature_info():
    with open("/tmp/weather-beijing.json", encoding="utf-8") as f:
        data = json.load(f)

    array_2011 = np.asarray(data["infos"]["2011"])
    fig = plt.figure(1)
    # 绘制折线图
    fig, ax = plt.subplots()
    ax.set_ylabel("Temprature(°C)")
    ax.plot(array_2011[0], array_2011[1], label="2011")
    ax.plot(array_2011[0], array_2011[2], label="2011")

    ax.legend()
    plt.savefig("weather.png", dpi=fig.dpi)
