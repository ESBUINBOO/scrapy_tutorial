import scrapy
from scrapy.linkextractors import LinkExtractor


class ExcersisesSpider(scrapy.Spider):
    name = "w3"
    start_urls = [
        # 'https://www.w3resource.com/python-exercises/',
        'https://www.w3resource.com/python-exercises/pandas/practice-set1/index.php',
    ]

    def parse(self, response):
        # links = LinkExtractor(allow=[r'/python-exercises/\w+/.*']).extract_links(response)
        for p in response.xpath('//p'):
            yield {
                'number':  p.xpath('./strong[1]').get(),
                'text': p.get(),
                'topic': response.url.split("/")[4]
            }
        # for a in response.css('li a'):
        # for a in links:
        #     self.logger.info('response.url=%s' % response.url)
        #     yield response.follow(a, callback=self.parse)
