from scrapy import Spider, Request


class BooksSpider(Spider):
    name = 'books'
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        for link in response.css('article > div > a::attr(href)').getall():
            yield Request(response.urljoin(link), callback=self.parse_item)
        for link in response.css('.next > a'):
            yield response.follow(link, self.parse)

    def parse_item(self, response):
        return {
            'title': response.css('h1').get(),
            'image': response.urljoin(
                response.css('.active > img::attr(src)').get()
            ),
            'price': response.css('.price_color').get(),
        }
