import os
import dotenv

from flask import Flask, request, render_template

from utils.scraper import CryptoScraper
from utils.summarizer import Summarizer

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
    results = await scraper.scrap(query)

    for result in results:
        news = News(
            url       = result['url'],
            heading   = result['heading'],
            paragraph = result['paragraph']
        )
        
        news.sync()
    
    return results

async def summary(title, url):
    
    pass

@app.route('/coin', methods=['GET'])
async def search():
    query   = request.args.get('q')
    s_index = request.args.get('s')
    
    if not query and not s_index:
        return render_template('search.html')
    
    data = await scrap(query)

    if s_index:
        news = data[s_index]

        if news:
            title = news['title']
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