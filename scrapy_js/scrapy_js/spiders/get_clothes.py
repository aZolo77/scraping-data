import scrapy
from scrapy_splash import SplashRequest

class GetClothesSpider(scrapy.Spider):
    name = 'get_clothes'
    allowed_domains = ['scrapingclub.com']
    # start_urls = ['https://scrapingclub.com/exercise/detail_sign/']
    
    script = '''
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(1))
          return {
            html = splash:html()
          }
        end
    '''
    
    def start_requests(self):
        yield SplashRequest(
            url='https://scrapingclub.com/exercise/detail_sign/',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        item = {}
        
        item['name'] = response.xpath("//h4[contains(@class, 'card-title')]/text()").get()
        item['price'] = response.xpath("//h4[contains(@class, 'card-price')]/text()").get()
        item['description'] = response.xpath("//p[contains(@class, 'card-description')]/text()").get()
        item['image'] = response.urljoin(response.xpath("//img[contains(@class, 'card-img-top')]/@src").get())
        
        return item
