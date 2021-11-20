from bs4 import BeautifulSoup
from .extracter import HTMLExtracter

class CryptoScraper:
    def __init__(self):
        self.base_url = 'https://www.coingecko.com/en/coins/%s/news'

    async def __extract_html(self, crypto_name):
        url = self.base_url % crypto_name.lower()
        extracter = HTMLExtracter(url, params={})

        return await extracter.extract()

    def __scrap_urls(self, div):
        headers = div.find_all('header')
        return [header.find('a')['href'] for header in headers]

    def __scrap_headings(self, div):
        headers = div.find_all('header')
        return [header.find('a').text for header in headers]

    def __scrap_paragraphs(self, div):
        paragraphs = div.find_all('div', {'class': 'post-body'})
        return [paragraph.text for paragraph in paragraphs]

    async def scrap(self, crypto_name):
        html = await self.__extract_html(crypto_name)
        soup = BeautifulSoup(html, 'html.parser')

        raw_news = soup.find('div', {'id': 'news'})
        
        if not raw_news:
            return []
        
        urls = self.__scrap_urls(raw_news)
        headings = self.__scrap_headings(raw_news)
        paragraphs = self.__scrap_paragraphs(raw_news)

        scrapped_news = []

        for index in range(10):
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
