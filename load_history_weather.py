"""
Load weather info for https://lishi.tianqi.com/
"""
import argparse
import asyncio
import json

from playwright.async_api import Playwright, async_playwright

from utils import create_console_logger


logger = create_console_logger()


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

    # Open new page
    page = await context.new_page()

    # Go to the chosen website
    await page.goto(args.url)
    await page.wait_for_load_state("networkidle")
    title = await page.title()
    content = await page.content()
    logger.info("page.title: %s", title)

    weather_info = await page.evaluate("[timeaxis, lowtemp, hightemp]")
    logger.info("var hightemp = %s", weather_info)

    if args.verbose:
        with open("/tmp/weather.html", encoding="utf-8", mode="w") as f:
            f.write(content)

    with open("/tmp/weather.json", encoding="utf-8", mode="w") as f:
        json.dump({"page": args.url, "weather": weather_info}, f, ensure_ascii=False)

    await context.close()
    # Turn off the browser once you finished
    await browser.close()


async def main() -> None:
    """Main Function"""
    parser = argparse.ArgumentParser(description="parse arg from cli")
    parser.add_argument("--url", help="Page to parse", default="https://lishi.tianqi.com/chengdu/202303.html")
    parser.add_argument(
        "-s", "--selector", help="A selector to use when resolving DOM element", default="//div[@class='thrui']"
    )
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logger.info("Parsing page: %s", args.url)
        logger.info("selector for chapters: %s", args.selector)

    async with async_playwright() as playwright:
        await run(playwright, args)


asyncio.run(main())
