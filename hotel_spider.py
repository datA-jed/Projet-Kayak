import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector

cities_list = ["Cassis", "Marseille", "Saintes+Maries+de+la+mer", "Collioure", "La+Rochelle"]

for i in range(len(cities_list)):

    class LinkSpider(scrapy.Spider):
        name = "link_hotel"

        start_urls = [
            "https://www.booking.com/searchresults.html?ss={}&nflt=ht_id=204".format(cities_list[i]),
        ]

        def parse(self, response):
                hotels = response.css("div[class='f6e3a11b0d ae5dbab14d e95943ce9b d32e843a31']")
                for hotel in hotels:
                    hotel_url = hotel.css("a[class='bd77474a8e']").attrib["href"]
                    yield {
                        'hotel_url': hotel_url
                    }



    filename = "hotel_links_{}.json".format(cities_list[i])

    if filename in os.listdir('data_collection_kayak/hotels_links/'):
                os.remove('data_collection_kayak/hotels_links/'+filename)

    process = CrawlerProcess(settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': logging.INFO,
        "FEEDS": {
            'data_collection_kayak/hotels_links/'+filename : {"format": "json"},
        },
        'DOWNLOAD_FAIL_ON_DATALOSS' : True,
        'RETRY_ENABLED' : True
    })

    process.crawl(LinkSpider)
process.start()