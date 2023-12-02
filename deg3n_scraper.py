from playwright.async_api import async_playwright
import asyncio
import sys

class deg3n_scraper():

    def __init__(self):
        self._browser = None
        self._page = None

    def __del__(self):
        if self._browser is not None:
            self._browser.close()
        else:
            pass

    async def browser_setup(self):
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=True)
        self._browser = browser

    async def page_setup(self):
        context = await self._browser.new_context(storage_state='data/state.json',viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        self._page = page

    async def _visit(self,url: str):
        await self._page.goto(url)
        twimg = self._page.get_by_test_id("tweetPhoto").first
        child = twimg.locator('xpath=child::*').first
        return (await child.get_attribute("style"))

    async def twimg_parse(self,url: str):
        data = await self._visit(url)
        url_parse = data.split('"')[1].split("&name")[0]
        return url_parse

if __name__ == "__main__":
    urls = ["https://twitter.com/shinoillust_/status/1728831175479935257","https://twitter.com/3saku_39/status/1729449221508796657?t=CogEUyVF0RObSqT4-HmUDg&s=19","https://twitter.com/momoco_haru/status/1729499671284924903?t=69VOg9ZEKE0pzjq6wLILYg&s=19", "https://x.com/Yampahood/status/1729403735766651253"]
    b1 = deg3n_scraper()
    for url in urls:
        print(b1.twimg_parse(url))
