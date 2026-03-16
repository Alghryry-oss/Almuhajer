import asyncio
from playwright.async_api import async_playwright
import random
from config import PROXY_LIST, USER_AGENTS
from .utils import random_delay

class StealthCrawler:
    def __init__(self, proxy=None, headless=True):
        self.proxy = random.choice(PROXY_LIST) if PROXY_LIST else None
        self.user_agent = random.choice(USER_AGENTS)
        self.headless = headless
    
    async def scrape_profile(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                user_agent=self.user_agent,
                proxy={'server': self.proxy} if self.proxy else None,
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            await page.goto(url, wait_until='networkidle')
            
            # Extract hidden data (emails, phones from page source)
            content = await page.content()
            # Use regex or BeautifulSoup to find emails/phones
            # ...
            
            # Simulate human behavior
            await page.mouse.move(random.randint(100,500), random.randint(100,500))
            random_delay(2,5)
            
            # Take screenshot
            await page.screenshot(path='data/screenshot.png')
            
            await browser.close()
            return content
    
    def run(self, url):
        return asyncio.run(self.scrape_profile(url))