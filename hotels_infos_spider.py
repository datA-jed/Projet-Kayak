import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector
import json
import time

cities_list = ["Cassis", "Marseille", "Saintes+Maries+de+la+mer", "Collioure", "La+Rochelle"]

for i in range(len(cities_list)):


    class HotelinfoSpider(scrapy.Spider):
        name = "link_hotel"

        with open("data_collection_kayak/hotels_links/hotel_links_{}.json".format(cities_list[i])) as f:
            urls = json.load(f)
            start_urls = [line['hotel_url'] for line in urls]

        def parse(self, response):
                time.sleep(0.3)
                yield {
                    "hotel_name" : response.css("h2[class='ddb12f4f86 pp-header__title']::text").get(),
                    "url_hotel" : response.url,
                    "hotel_coordinates" : response.css("a[id='map_trigger_header']::attr(data-atlas-latlng)").get(),
                    "score" : response.css("div[class='f63b14ab7a dff2e52086']::text").get().replace(',', '.'),
                    "text_description" : response.css("p[class='b99b6ef58f f1152bae71']::text").get(),
                    "address" : response.css("div[class='b99b6ef58f cb4b7a25d9']::text").get()
                }
                


    filename = "hotels_infos_{}.json".format(cities_list[i])

    if filename in os.listdir('data_collection_kayak/hotels_infos_per_city/'):
                os.remove('data_collection_kayak/hotels_infos_per_city/'+filename)

    process = CrawlerProcess(settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': logging.INFO,
          'DEFAULT_REQUEST_HEADERS': {
        'Accept-Language': 'fr-FR,fr;q=0.9'
        },
        "FEEDS": {
            'Scraping/hotels_infos_per_city/'+filename : {"format": "json", "encoding": "utf-8",},
        },
        'DOWNLOAD_FAIL_ON_DATALOSS' : True,
        'RETRY_ENABLED' : True
    })

    process.crawl(HotelinfoSpider)
process.start()