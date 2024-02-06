import argparse
import asyncio
import json
from typing import Any, Dict, List

from playwright.async_api import Playwright, async_playwright


# Start with playwright scraping here:
async def scrape_data(page, args: argparse.Namespace) -> List[Dict[str, Any]]:
    """提取 Chapter 信息的函数

    Parameters
    ----------
    batch_size: each element in the dataloader iterable will return a batch of <batch_size> features and labels.
        default is 64

    Returns
    -------
    train_dataloader : data for train
    test_dataloader : data for test
    """
    scraped_elements = []
    # div.dl.dd.a in <div class="box_con">
    # <div id="list"><dl><dd><a href="...">title</a>
    locators = await page.locator(args.selector).all()
    if args.verbose:
        print("=" * 10, "find", len(locators), "items")

    # Pick the scraping item
    for i, locator in enumerate(locators):
        scraped_element = {"index": i}
        scraped_element["title"] = await locator.inner_text()

        # Chapter link
        scraped_element["link"] = await locator.get_attribute("href")

        scraped_elements.append(scraped_element)
    return scraped_elements


async def run(playwright: Playwright, args: argparse.Namespace) -> None:
    """Playwright 主函数

    Parameters
    ----------
    playwright

    args: Input from command line
    """
    # chromium.launch - opens a Chromium browser: headless=False, args=["--enable-javascript", "--enable-cookies"]
    browser = await playwright.chromium.launch(headless=False)

    # Creates a new browser context
    context = await browser.new_context()

    # Open new page
    page = await context.new_page()

    # Go to the chosen website
    await page.goto(args.url)
    await page.wait_for_load_state("networkidle")
    title = await page.title()
    content = await page.content()
    print("page.title:", title)

    if args.verbose:
        with open("/tmp/chapters.html", mode="w") as f:
            f.write(content)

    data = await scrape_data(page, args)

    with open("/tmp/chapters.json", "w") as f:
        json.dump({"page": args.url, "chapters": data}, f, indent=2, ensure_ascii=False)

    await context.close()
    # Turn off the browser once you finished
    await browser.close()


async def main() -> None:
    parser = argparse.ArgumentParser(description="parse arg from cli")
    parser.add_argument("--url", help="Page to parse", default="https://www.ibiquges.org/26/26625/")
    parser.add_argument("-s", "--selector", help="A selector to use when resolving DOM element", default="dl dd a")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        print("Parsing page:", args.url)
        print("selector for chapters:", args.selector)

    async with async_playwright() as playwright:
        await run(playwright, args)


asyncio.run(main())
