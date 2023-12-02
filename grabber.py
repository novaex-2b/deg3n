from playwright.async_api import async_playwright
import asyncio
import sys

async def scrape_tweet(url: str) -> dict:
    """
    Scrape a single tweet page for Tweet thread e.g.:
    https://twitter.com/Scrapfly_dev/status/1667013143904567296
    Return parent tweet, reply tweets and recommended tweets
    """

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="data/state.json",viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        # enable background request intercepting:
        # go to url and wait for the page to load
        await page.goto(url)
        twimg = page.get_by_test_id("tweetPhoto").first
        child = twimg.locator('xpath=child::*').first
        found_url = await child.get_attribute("style",timeout=0)
        return found_url

async def twimg_parse(url: str) -> str:
    print("Received this URL to parse: {}".format(url))
    data = await scrape_tweet(url)
    return data.split('"')[1].split("&name")[0]

if __name__ == "__main__":
    url = sys.argv[1]
    print(asyncio.run(twimg_parse(url)))
