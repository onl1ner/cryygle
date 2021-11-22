from bs4 import BeautifulSoup

from utils.scrapers.scraper import Scraper

class ArticleScraper(Scraper):
    def __init__(self):
        super().__init__()
    
    async def scrap(self, **kwargs):
        if not 'article_url' in kwargs: return 'Failed to parse HTML'

        article_url = kwargs.get('article_url')
        
        html = await super()._extract_html(article_url)
        soup = BeautifulSoup(html, 'html.parser')

        raw_tags  = soup.find_all(['h1', 'p'])
        tag_texts = [tag.text for tag in raw_tags]

        return ' '.join(tag_texts)

    pass