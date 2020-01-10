import scrapy
from scrapy.linkextractors import LinkExtractor


class SpiegelSpider(scrapy.Spider):
    name = "spiegel"
    start_urls = [
        'https://www.spiegel.de/'
    ]

    def parse(self, response):
        links = LinkExtractor(allow=[r'/politik/\w+/.*',
                                     r'/meinung/\w+/.*',
                                     r'/wirtschaft/\w+/.*',
                                     r'/panorama/\w+/.*',
                                     r'/sport/\w+/.*',
                                     r'/kultur/\w+/.*',
                                     r'/netzwelt/\w+/.*',
                                     r'/wissenschaft/\w+/.*',
                                     r'/gesundheit/\w+/.*',
                                     r'/geschichte/\w+/.*',
                                     r'/lebenundlernen/\w+/.*',
                                     r'/reise/\w+/.*',
                                     r'/auto/\w+/.*',
                                     r'/stil/\w+/.*'],
                              allow_domains=['spiegel.de'],
                              deny=[r'^(.(?!.*\.html))*$',
                                    r'^(.*\/archiv\.html$)',
                                    r'^(.*\/bild\-\d*)',
                                    r'^(.*\/grossbild\-\d.*\.html$)',
                                    r'^(.*\d\-druck\.html$)']).extract_links(response)
        element = response.xpath('//*[@id="content-main"]')
        try:
            yield {
                'title': element.xpath('./div/div/h2/span[@class="headline"]').get(),
                'intro':  element.xpath('//*[@class="article-intro"]').get(),
                'text': element.xpath('./div/div/p').getall(),
                'rubrik': response.url.split("/")[3],
                'kategorie': response.url.split("/")[4],
                'date': element.xpath('//*[@id="js-article-column"]/div/div[2]/span/time').get(),
                'url': response.url
            }
        except Exception as e:
            print(e)
        for a in links:
            self.logger.info('response.url=%s' % response.url)
            yield response.follow(a, callback=self.parse)
