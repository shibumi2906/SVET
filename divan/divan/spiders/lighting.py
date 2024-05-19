import scrapy

class LightingSpider(scrapy.Spider):
    name = 'lighting'
    allowed_domains = ['divan.ru']
    start_urls = ['https://www.divan.ru/category/svet']

    def parse(self, response):
        self.log(f'Parsing page: {response.url}')
        # Используем CSS селектор для извлечения ссылок на продукты
        product_links = response.css('a[href*="/product/"]::attr(href)').getall()
        self.log(f'Found {len(product_links)} product links')

        for link in product_links:
            yield response.follow(link, self.parse_product)

        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            self.log(f'Next page found: {next_page}')
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        name = response.css('h1[itemprop="name"]::text').get()
        price = response.css('span[itemprop="price"]::attr(content)').get()

        if name and price:
            yield {
                'name': name,
                'price': price,
                'link': response.url
            }

# В settings.py добавьте следующую строку, чтобы сохранить данные в CSV файл:
FEED_FORMAT = 'csv'
FEED_URI = 'lighting.csv'





