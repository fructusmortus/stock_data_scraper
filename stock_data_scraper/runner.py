from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from stock_data_scraper import settings
from stock_data_scraper.spiders.finviz import FinvizSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(FinvizSpider)
    process.start()
