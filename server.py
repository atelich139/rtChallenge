import asyncio
import json

from flask import Flask, request, Response
from utilities import Utilities
from scraper import Scraper


class Server:
    app = Flask(__name__)

    @app.route('/reviews', methods=['POST'])
    def reviews():
        raw = request.form['url']

        if Utilities.valid_url(raw):
            pass
        else:
            return Response("", status=400)

        scraper = Scraper(raw)
        reviews = asyncio.run(scraper.get_reviews())
        output = json.dumps(reviews)

        return Response(output, status=200, mimetype='application/json')
