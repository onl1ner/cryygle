from abc import ABC, abstractmethod
from ..extracter import HTMLExtracter

class Scraper(ABC):
    def __init__(self):
        super().__init__()
    
    async def _extract_html(self, url):
        return await HTMLExtracter(url).extract()

    @abstractmethod
    async def scrap(self, **kwargs): pass

    pass