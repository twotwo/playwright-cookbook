import argparse
import asyncio
import json

from playwright.async_api import Playwright, async_playwright


# Start with playwright scraping here:
async def scrape_data(page, args: argparse.Namespace):
    scraped_elements = []
    # div.dl.dd.a in <div class="box_con">
    # <div id="list"><dl><dd><a href="...">title</a>
    locators = await page.locator("dl dd a").all()
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
    # chromium.launch - opens a Chromium browser: headless=False, args=["--enable-javascript", "--enable-cookies"]
    browser = await playwright.chromium.launch(headless=False)

    # Creates a new browser context
    context = await browser.new_context()

    # Open new page
    page = await context.new_page()

    # Go to the chosen website
    await page.goto(args.url)
    await page.wait_for_load_state("networkidle")
    print("domcontentloaded")  # networkidle
    content = await page.content()
    with open("/tmp/content.html", mode="w") as f:
        f.write(content)
    data = await scrape_data(page, args)

    with open("/tmp/chapters.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    await context.close()
    # Turn off the browser once you finished
    await browser.close()


async def main() -> None:
    parser = argparse.ArgumentParser(description="parse arg from cli")
    parser.add_argument("--url", help="Page to parse", default="https://www.ibiquges.org/26/26625/")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        print("Parsing page:", args.url)

    async with async_playwright() as playwright:
        await run(playwright, args)


asyncio.run(main())
