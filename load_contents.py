import argparse
import asyncio
import json
import os
import random
from urllib.parse import urljoin

from playwright.async_api import Playwright, async_playwright


async def load_by_page(context, args: argparse.Namespace) -> None:
    with open("/tmp/chapters.json") as f:
        chapters = json.load(f)
    base_url = chapters["page"]
    # print(chapters["page"], chapters["chapters"][0])
    random_number = random.randint(30, 60)
    page = await context.new_page()  # Open new page
    for chapter in chapters["chapters"]:
        print("parse", chapter)
        html_file = f"/tmp/book/{chapter['index']}-{chapter['title']}.html"
        if os.path.exists(html_file):
            continue
        response = await page.goto(urljoin(base_url, chapter["link"]))  # Go to the chosen website
        print(response.url, "STATUS", response.status)
        if response.status > 500:
            await asyncio.sleep(random_number)
            continue

        # content = await page.content()
        # with open("/tmp/content.html", mode="w") as f:
        #     f.write(content)

        # You scraping functions go here
        locator = page.locator(args.selector)  # <div id="content"

        html_content = await locator.inner_html()
        # print("=" * 10, html_content)
        with open(html_file, mode="w") as f:
            f.write(html_content)

        context.set_default_navigation_timeout(30000)
        await asyncio.sleep(5)  # sleep 5 seconds


async def run(playwright: Playwright, args: argparse.Namespace) -> None:
    """Playwright 主函数

    Parameters
    ----------
    playwright

    args: Input from command line
    """
    # Launch the headed browser instance (headless=False)
    # To see the process of playwright scraping
    # chromium.launch - opens a Chromium browser
    browser = await playwright.chromium.launch(headless=args.headless)
    context = await browser.new_context()  # Creates a new browser context

    await load_by_page(context, args)

    # Turn off the browser and context once you have finished
    await context.close()
    await browser.close()


async def main() -> None:
    parser = argparse.ArgumentParser(description="parse arg from cli")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--info", help="Chapter info", default="/tmp/chapters.json")
    parser.add_argument("--start", help="index for chapters", default=0)
    parser.add_argument("-s", "--selector", help="A selector to use when resolving DOM element", default="id=content")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        print("Parsing page:", args.url)
        print("selector for content:", args.selector)

    async with async_playwright() as playwright:
        await run(playwright, args)


asyncio.run(main())
