"""
Load weather info for https://lishi.tianqi.com/
"""
import argparse
import asyncio
import datetime
import json

from playwright.async_api import Playwright, async_playwright

from utils import create_console_logger


logger = create_console_logger()


def _gen_url(city: str, year: int, month: int):
    # https://lishi.tianqi.com/chengdu/202303.html
    return f"https://lishi.tianqi.com/{city}/{year}{month:02d}.html"


async def load_by_page(context, args: argparse.Namespace) -> None:
    # Open new page
    page = await context.new_page()
    infos = {}

    for year in range(int(args.year), datetime.datetime.now().year + 1):
        url = _gen_url(args.city, year, args.month)
        # Go to the chosen website
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        title = await page.title()
        content = await page.content()
        logger.info("page.title: %s", title)

        weather_info = await page.evaluate("[timeaxis, lowtemp, hightemp]")
        logger.info("axis, low, high = %s", weather_info)
        infos[year] = weather_info

        await asyncio.sleep(2.5)  # sleep 2.5 seconds

    if args.verbose:
        with open("/tmp/weather.html", encoding="utf-8", mode="w") as f:
            f.write(content)

    with open(f"/tmp/weather-{args.city}.json", encoding="utf-8", mode="w") as f:
        json.dump({"city": args.city, "month": args.month, "infos": infos}, f, ensure_ascii=False)


async def run(playwright: Playwright, args: argparse.Namespace) -> None:
    """Playwright 主函数

    Parameters
    ----------
    playwright

    args: Input from command line
    """
    # chromium.launch - opens a Chromium browser: headless=False
    browser = await playwright.chromium.launch()

    # Creates a new browser context
    context = await browser.new_context()

    await load_by_page(context, args)

    await context.close()
    # Turn off the browser once you finished
    await browser.close()


async def main() -> None:
    """Main Function"""
    parser = argparse.ArgumentParser(description="parse arg from cli")
    parser.add_argument("--city", help="pinyin of the city", default="beijing")
    parser.add_argument("--year", help="start year", default=2011)
    parser.add_argument("--month", help="month of the weather info", default=3)
    parser.add_argument(
        "-s", "--selector", help="A selector to use when resolving DOM element", default="//div[@class='thrui']"
    )
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logger.info("Parsing page: %s", _gen_url(args.city, args.year, args.month))
        logger.info("selector for chapters: %s", args.selector)

    async with async_playwright() as playwright:
        await run(playwright, args)


asyncio.run(main())

# python load_history_weather.py --city chengdu
