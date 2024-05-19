import scrapy

class LightingSpider(scrapy.Spider):
    name = 'lighting'
    allowed_domains = ['divan.ru']
    start_urls = ['https://www.divan.ru/category/svet']

    def parse(self, response):
        # Ищем ссылки на отдельные страницы с источниками освещения
        product_links = response.css('a.product-card__link::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, self.parse_product)

        # Переход на следующую страницу, если она есть
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        # Извлечение информации о товаре
        yield {
            'name': response.css('h1.product-card__name::text').get(),
            'price': response.css('span.product-card__price::text').get(),
            'link': response.url
        }