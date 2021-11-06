import asyncio

from flask import Flask, render_template, request, redirect
from utils.scraper import Scraper

app = Flask(__name__)

async def scrap(query):
    scraper = Scraper()
    return await scraper.scrap(query, 100)

@app.route('/search', methods=['GET'])
async def search():
    query = request.args.get('q')

    if not query:
        return render_template('search.html')
    
    return render_template('search.html', query=query, data=await scrap(query))

if __name__ == "__main__":
    app.run(debug=True)