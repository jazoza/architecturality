from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from scrapy.http import Request
from dezeen.items import DezeenItem


class DezeenSpider(CrawlSpider):
    name = "dezeentech"
    allowed_domains = ["dezeen.com"]
    start_urls = ["https://www.dezeen.com/technology/"]
    rules = (
        Rule(LinkExtractor(allow=('page/*'), ), callback="get_all_links", follow= True),
    )

    def get_all_links(self, response):
        hxs = Selector(response)
        titles = hxs.xpath("//article/header/a")
        items = []
        for titles in titles:
            item = DezeenItem()
            item["link"] = titles.xpath("@href").extract()
            items.append(item)
        for link in items:
            #print(link["link"][0])
            url = link["link"][0]
            print("this is the url", url, "\n")
            yield Request(url=url, meta={'item': item}, callback=self.parse_item_page)

    def parse_item_page(self, response):
        page = Selector(response)
        item=response.meta['item']
        item['description'] = page.xpath("//p/text()").extract()
        #content = page.xpath("//p")
        print("{", ('').join(item['link']), ":", (' ').join(item['description']), "}", "\n")
