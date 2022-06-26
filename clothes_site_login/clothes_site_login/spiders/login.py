import scrapy
from scrapy import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/basic_login']

    def parse(self, response):
        token = response.xpath("//input[@name='csrfmiddlewaretoken']/@value").get()
        
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'name': 'scrapingclub',
                'password': 'scrapingclub',
                'csrfmiddlewaretoken': token
            },
            callback=self.get_data
        )

        
    def get_data(self, response):
        print('===========  Logged in  ===========')
        success_text = response.xpath('//nav[contains(@class, "navbar")]/following-sibling::div/div/div/div[2]/p/text()').get()
        return {
            'success': success_text
        }