from bs4 import BeautifulSoup
from .extracter import HTMLExtracter

class Scraper:
    def __init__(self):
        self.base_url = 'https://google.com/search'

    async def __extract_html(self, crypto_name, page_limit):
        params = {
            'q': 'site:coinmarketcap.com %s' % crypto_name,
            'hl': 'ru-RU',
            'source': 'lnms',
            'tbm': 'nws',
            'num': page_limit
        }

        extracter = HTMLExtracter(self.base_url, params)
        return await extracter.extract()

    def __scrap_urls(self, div):
        urls = div.find_all('a', {'class': 'WlydOe'})
        return [url['href'] for url in urls]

    def __scrap_headings(self, div):
        headings = div.find_all('div', {'role': 'heading'})
        return [heading.text for heading in headings]

    def __scrap_paragraphs(self, div):
        paragraphs = div.find_all('div', {'class': 'GI74Re nDgy9d'})
        return [paragraph.text for paragraph in paragraphs]

    async def scrap(self, crypto_name, page_limit):
        html = await self.__extract_html(crypto_name, page_limit)
        soup = BeautifulSoup(html, 'html.parser')
        
        raw_news = soup.find('div', {'id': 'rso'})

        if not raw_news:
            return []
        
        urls = self.__scrap_urls(raw_news)
        headings = self.__scrap_headings(raw_news)
        paragraphs = self.__scrap_paragraphs(raw_news)

        scrapped_news = []

        for index in range(page_limit):
            url = urls[index]
            heading = headings[index]
            paragraph = paragraphs[index]

            scrapped_news.append({
                'url': url,
                'heading': heading,
                'paragraph': paragraph
            })

        return scrapped_news

    pass
