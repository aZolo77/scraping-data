import scrapy
from scrapy_splash import SplashRequest

class GetQuotesSpider(scrapy.Spider):
    name = 'get_quotes'
    allowed_domains = ['quotes.toscrape.com']
    
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
            url='https://quotes.toscrape.com/js/',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        all_quotes = response.xpath("//div[@class='quote']")
        
        for i, q in enumerate(all_quotes):
            tags_lst = q.xpath(".//a[@class='tag']")
            item = {
                'text': q.xpath(".//span[@class='text']/text()").get(),
                'author': q.xpath(".//span/small[@class='author']/text()").get(),
                'tags': [t.xpath(".//text()").get() for t in tags_lst]
            }
            
            yield item
        
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield SplashRequest(
                url=next_page_url,
                callback=self.parse,
                endpoint='execute',
                args={
                    'lua_source': self.script
                }
            )
