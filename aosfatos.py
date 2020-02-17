import scrapy

class AosFatosSpider(scrapy.Spider):
    name ='aos_fatos'

    start_urls = ['https://aosfatos.org']

    def parse(self,response):
        links = response.xpath(
            '//div[@class="openmenu"]//ul/li/a[re:test(@href,"checamos")]/@href').getall()   
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_news_page
            )

    def parse_news_page(self,response):
        new_links = response.css('.card::attr(href)').getall()
        for new_link in new_links:
            yield scrapy.Request(
                response.urljoin(new_link),
                callback = self.parser_new
            )

        pagination_link = response.css('.pagination a::attr(href)').getall()
        for next_page_link in pagination_link:
            yield scrapy.Request(
                response.urljoin(next_page_link),
                callback=self.parse_news_page
            )        
    
    def parser_new(self,response):
        quotes = response.css('article blockquote p')
        for quote in quotes:
            status = quote.xpath('./parent::blockquote/preceding-sibling::figure//figcaption[string-length(normalize-space(text()))>0]/text()'
            ).get()
            yield{
                'title': response.css('article h1::text').get().replace(";",""),
                'date': ' '.join(response.css('p.publish_date::text').get().split()),
                'quote': quote.css('::text').get(),
                'status': status,
                'url': response.url
            }

            