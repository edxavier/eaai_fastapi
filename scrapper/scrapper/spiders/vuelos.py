import scrapy


class VuelosSpider(scrapy.Spider):
    name = "vuelos"
    allowed_domains = ["eaai.com.ni"]
    start_urls = ["https://www.eaai.com.ni/fids/vuelos_dias_fids.php?option=A"]

    def parse(self, response):
        print(response.text)
