import asyncio
import pyppeteer

from requests_html import AsyncHTMLSession

class HTMLExtracter:
    def __init__(self, base_url, params):
        self.base_url = base_url
        self.params = params

        self.session = AsyncHTMLSession()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'
        }

    async def extract(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        
        browser = await pyppeteer.launch({ 
            'ignoreHTTPSErrors':True, 
            'headless':True, 
            'handleSIGINT':False, 
            'handleSIGTERM':False, 
            'handleSIGHUP':False
        })

        self.session._browser = browser

        response = await self.session.get(
            self.base_url, headers=self.headers, params=self.params
        )

        await response.html.arender(timeout = 20)

        return response.html.raw_html
        
    pass
