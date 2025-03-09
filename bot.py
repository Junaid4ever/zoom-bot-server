import asyncio
import sys
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from faker import Faker
import nest_asyncio

nest_asyncio.apply()
faker = Faker("en_IN")

async def start(wait_time, meetingcode, passcode, browser):
    async with browser.new_context() as context:
        page = await context.new_page()
        await page.goto(f'http://app.zoom.us/wc/join/{meetingcode}')
        await page.fill('input[type="text"]', faker.name())
        if await page.query_selector('input[type="password"]'):
            await page.fill('input[type="password"]', passcode)
        await page.click('button.preview-join-button')
        await asyncio.sleep(wait_time)

async def main():
    meetingcode, passcode, num_users = sys.argv[1:4]
    num_users = int(num_users)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [start(3600, meetingcode, passcode, browser) for _ in range(num_users)]
        await asyncio.gather(*tasks)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
