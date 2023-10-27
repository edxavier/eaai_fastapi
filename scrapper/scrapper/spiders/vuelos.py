import scrapy


class VuelosSpider(scrapy.Spider):
    name = "vuelos"
    allowed_domains = ["eaai.com.ni"]
    start_urls = ["https://www.eaai.com.ni/fids/vuelos_dias_fids.php?option=A"]

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.eaai.com.ni/fids/vuelos_dias_fids.php?option=A',
            meta={'playwright': True},
            callback=self.parse, errback=self.errback_close_page)

    async def parse(self, response):
        print(response.text)

    async def errback_close_page(self, response):
        page = response.request
        print(page)
        print(response)

