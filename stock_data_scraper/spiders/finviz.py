import scrapy
import json
from scrapy.http import HtmlResponse
from collections import Counter

from stock_data_scraper.items import FinvizItem


class FinvizSpider(scrapy.Spider):
    name = 'finviz'
    allowed_domains = ['finviz.com']
    start_urls = ['https://finviz.com/screener.ashx']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a/b[contains(text(), 'next')]/../@href").extract_first()

        companies_links = response.xpath("//a[@class='screener-link-primary']/@href").extract()
        for link in companies_links:
            yield response.follow(link, callback=self.parse_company)
        yield response.follow(next_page, callback=self.parse)

    def parse_company(self, response: HtmlResponse):
        ticker = response.xpath("//a[@class='fullview-ticker']/text()").extract_first()
        full_name = response.xpath("//td[@align='center']/a[not(@onclick)]/b/text()").extract_first()
        sector = response.xpath("(//td[@align='center' ][@class='fullview-links'])[1]/a[1]/text()").extract_first()
        industry = response.xpath("(//td[@align='center' ][@class='fullview-links'])[1]/a[2]/text()").extract_first()
        country = response.xpath("(//td[@align='center' ][@class='fullview-links'])[1]/a[3]/text()").extract_first()
        table_el_keys = response.xpath("//tr/td[@class='snapshot-td2-cp']/text()").extract()
        table_el_values = response.xpath(
            "//td[@class='snapshot-td2']/b/text() | //td[@class='snapshot-td2']/b/span/text() | "
            "//td[@class='snapshot-td2']/b/small/text()").extract()
        d = {a: list(range(1, b + 1)) if b > 1 else '' for a, b in Counter(table_el_keys).items()}
        table_el_keys = [i + str(d[i].pop(0)) if len(d[i]) else i for i in table_el_keys]
        table1_temp = {}
        for k, v in zip(table_el_keys, table_el_values):
            table1_temp[k] = v
        yield FinvizItem(ticker=ticker,
                         full_name=full_name,
                         sector=sector,
                         industry=industry,
                         country=country,
                         table1=table1_temp)
