#==> Importando biblioteca
import scrapy

#==> Classe para webscraping e crawlers 
class RondoniaNoticiasSpider(scrapy.Spider):
    name = "rondonia_noticias"
    allowed_domains = ["rondoniadinamica.com"]
    start_urls = ["https://rondoniadinamica.com/ultimas-noticias"]

    #==> Definindo dados a ser recuperados
    def parse(self, response):
        for tag in response.css('div.post-data'):
            yield {
                'noticia': tag.css('a.post-title h6 strong::text').get(),
                'publicacao': tag.css('a.post-catagory::text').get(),
                'link': tag.css('a.post-title::attr(href)').get(),
            }
            
        #==> Recuperando link da proxima pagina
        proxima_pagina = response.css('ul.pagination .page-item a.page-link::attr(href)').getall()

        #==> Recuperando dados de ate 3 paginas
        if proxima_pagina and len(proxima_pagina) >= 3:
            # Faz a requisição apenas para a terceira página
            url_proxima_pagina = response.urljoin(proxima_pagina[1])  # Pega a segunda página (index 1)
            yield response.follow(url=url_proxima_pagina, callback=self.parse)