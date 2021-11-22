import os
import dotenv

from flask import Flask, request, render_template

from utils.summarizer import Summarizer

from utils.scrapers.crypto_scraper import CryptoScraper
from utils.scrapers.article_scraper import ArticleScraper

from utils.database import db

from models.news import News

dotenv.load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

async def scrap(query):
    scraper = CryptoScraper()
    results = await scraper.scrap(crypto_name = query)

    for result in results:
        news = News(
            url       = result['url'],
            heading   = result['heading'],
            paragraph = result['paragraph']
        )
        
        news.sync()
    
    return results

async def summary(title, url):
    scraper = ArticleScraper()
    article = await scraper.scrap(article_url = url)
    
    summary = Summarizer(article).summarize()

    print(summary)

    return {
        'title': title,
        'summary': summary
    }

@app.route('/coin', methods=['GET'])
async def search():
    query   = request.args.get('q')
    s_index = request.args.get('s')
    
    if not query and not s_index:
        return render_template('search.html')
    
    data = await scrap(query)

    if int(s_index):
        news = data[s_index]

        if news:
            title = news['heading']
            url   = news['url']

            s = await summary(title, url)

            return render_template(
                'search.html',
                query   = query,
                data    = data,
                summary = s
            )

    return render_template('search.html', query = query, data = data)

if __name__ == "__main__":
    app.run(debug=True)