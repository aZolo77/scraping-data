import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlItemsSpider(CrawlSpider):
    name = 'crawl_items'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[contains(@class, 'active')]/following-sibling::li/a"), follow=True),  # переход между страницами товаров
        Rule(LinkExtractor(restrict_xpaths="//h4[@class='card-title']/a"), callback='parse_item', follow=True)  # ссылка на товар
    )

    def parse_item(self, response):
        item = {}
        
        item['name'] = response.xpath("//h3[contains(@class, 'card-title')]/text()").get()
        item['price'] = response.xpath("//div[contains(@class, 'card-body')]/h4/text()").get()
        item['description'] = response.xpath("//p[contains(@class, 'card-text')]/text()").get()
        item['img'] = response.urljoin(response.xpath("//img[contains(@class, 'card-img-top')]/@src").get())
        
        return item
