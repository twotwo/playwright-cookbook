import json
import os
from urllib.parse import urljoin

import pytest
from playwright.sync_api import Error, sync_playwright


def file_exists(file_path):
    return os.path.exists(file_path)


@pytest.mark.skipif(not file_exists("/tmp/chapters.html"), reason="file not exists")
def test_check_title_exists():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # 加载本地HTML文件
        page.goto("file:///tmp/chapters.html")
        print(page.content())
        page.wait_for_load_state("networkidle")
        print("dom content loaded")  # networkidle

        # 判断title字段是否存在
        assert page.locator("title") is not None

        # <div class="nav"><ul><li><a>...
        locator = page.locator("id=nav")
        print("locate locator:", locator)

        with pytest.raises(Error):  # assert TimeoutError
            print(locator.text_content(timeout=200))

        browser.close()


@pytest.mark.skipif(not file_exists("/tmp/chapters.json"), reason="file not exists")
def test_load_chapter_info():
    with open("/tmp/chapters.json") as f:
        chapters = json.load(f)
    assert chapters["page"] is not None
    print(chapters["page"], chapters["chapters"][0])
    assert (
        urljoin("https://www.ibiquges.org/26/26625/", "/26/26625/13066308.html")
        == "https://www.ibiquges.org/26/26625/13066308.html"
    )
