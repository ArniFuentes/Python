from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


# NOTA:Este código permite extraer el titular y una pequeña descrición inicial de las noticas de la url semilla, pero
# este código no ingresa a ninguna de las noticias (siempre trabaja en la url semilla)

class Noticia(Item):
    titular = Field()
    descripcion = Field()


class ElUniversoSpider(Spider):
    name = "Spider1"
    custom_settings = {
        'USER_AGENT': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
        Chrome/80.0.3987.149 Safari/537.36''',
        # ordenar las columnas en el CSV
        'FEED_EXPORT_FIELDS': ['titular', 'descripcion'],
    }
    # URL
    start_urls = ['https://www.eluniverso.com/deportes']

    def parse(self, response):
        html = Selector(response)
        noticias = html.xpath('//ul[@class="feed | divide-y relative  "]/li[@class="relative"]')
        for noticia in noticias:
            item = ItemLoader(Noticia(), noticia)
            item.add_xpath('descripcion', './/p/text()')
            item.add_xpath('titular', './/h2/a/text()')
            yield item.load_item()


# TERMINAR: scrapy runspider WebScrapingScrapy1.py -o base_de_datos.csv
            
