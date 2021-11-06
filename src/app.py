import asyncio

from flask import Flask, render_template, request, redirect
from utils.scraper import Scraper

app = Flask(__name__)

def scrap(query):
    scraper = Scraper()
    return scraper.scrap(query, 100)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')

    if not query:
        return render_template('search.html')
    
    return render_template('search.html', query=query, data=scrap(query))

if __name__ == "__main__":
    app.run(debug=True)