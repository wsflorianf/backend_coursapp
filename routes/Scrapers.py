import concurrent
import time
from datetime import datetime

from flask import Blueprint, request, jsonify
import concurrent.futures

from routes.Auth import verify_token_middleware
from utils.Scrapers.PlaziScraper import PlatziScraper
from utils.Scrapers.UdacityScraper import UdacityScraper
from utils.Scrapers.DomestikaScraper import DomestikaScraper
from utils.Scrapers.CourseraScraper import CourseraScraper
from utils.WebDriverManager import WebDriverManager

routes_scrap = Blueprint("routes_scrap", __name__)


@routes_scrap.route("/search", methods=['GET'])
@verify_token_middleware
def search_courses():
    query = request.args.get('search-query', default='', type=str)
    # Obtener los flags de activación para cada plataforma desde los parámetros de la URL
    udacity_enabled = request.args.get('udacity', 'false').lower() == 'true'
    coursera_enabled = request.args.get('coursera', 'false').lower() == 'true'
    domestika_enabled = request.args.get('domestika', 'false').lower() == 'true'
    platzi_enabled = request.args.get('platzi', 'false').lower() == 'true'

    results = {}
    times = {}

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = {}

        if udacity_enabled:
            scraper = UdacityScraper()
            start = datetime.now()
            future = executor.submit(scraper.scrape, query)
            futures[future] = ('udacity', start)

        if coursera_enabled:
            scraper = CourseraScraper()
            start = datetime.now()
            future = executor.submit(scraper.scrape, query)
            futures[future] = ('coursera', start)

        if domestika_enabled:
            scraper = DomestikaScraper()
            start = datetime.now()
            future = executor.submit(scraper.scrape, query)
            futures[future] = ('domestika', start)

        if platzi_enabled:
            scraper = PlatziScraper()
            start = datetime.now()
            future = executor.submit(scraper.scrape, query)
            futures[future] = ('platzi', start)

        for future in concurrent.futures.as_completed(futures):
            platform, start_time = futures[future]
            if platform not in results:
                results[platform] = []
            results[platform].extend(future.result())
            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()
            times[platform] = elapsed_time

    WebDriverManager.close_driver()
    return jsonify(results=results, times=times)

