import scrapy
import re
from scrapy.shell import inspect_response

class PesquisaCrawler(scrapy.Spider):
    name = 'pesquisa'
      
    start_urls = ['http://pesquisasaude.saude.gov.br/pesquisas.xhtml']
    
    def parse(self,response):
               
        view_state = response.xpath("//input[@id='javax.faces.ViewState']/@value").get()
        
        pagination = response.css('.next::attr(id)').get()

        # for i in range(0,1):
        #     yield scrapy.FormRequest(
        #         url = 'http://pesquisasaude.saude.gov.br/pesquisas.xhtml',
        #         formdata = {
        #             'form':'form',
        #             'javax.faces.ViewState': view_state,
        #             'javax.faces.source':pagination,
        #             'javax.faces.partial.event':'click',
        #             'javax.faces.partial.execute':pagination + ' form',
        #             'javax.faces.partial.render':'form',
        #             'javax.faces.behavior.event':'action',
        #             'javax.faces.partial.ajax': 'true'
        #         },
        #         callback = self.parse_page,
        #         dont_filter = True
        #     )
        
    # def parse_page(self, response):

        pesquisa_base_url = 'pesquisaView.xhtml?id='

        research_list = response.xpath('//button/@onclick').getall()
        
        research_id_list = [
            re.findall('\((\d+)\)',id)[0] for id in research_list
        ]
        research_links = [
            pesquisa_base_url + id for id in research_id_list 
        ]
            
        for link in research_links:      
            yield scrapy.Request(
                response.urljoin(link),
                callback = self.parse_data
            )

        
        # for i in range(0,1):
        #     yield scrapy.FormRequest(
        #         url = 'http://pesquisasaude.saude.gov.br/pesquisas.xhtml',
        #         formdata = {
        #             'form':'form',
        #             'javax.faces.ViewState': view_state,
        #             'javax.faces.source':pagination,
        #             'javax.faces.partial.event':'click',
        #             'javax.faces.partial.execute':pagination + ' form',
        #             'javax.faces.partial.render':'form',
        #             'javax.faces.behavior.event':'action',
        #             'javax.faces.partial.ajax': 'true'
        #         },
        #         callback = self.parse_new,
        #         dont_filter = True
        #     )

    def parse_data(self, response):
        inspect_response(response, self)
        yield{
        'title': response.url,
        'research_url': response.xpath('//div//p/span[@id="urlLattes"]/text()').get(),
        'uf': response.css('#uf::text').get(),
        'year': response.css('#ano::text').get(),
        'keywords': response.css('#palavraChave::text').get(),
        'sub_agenda': response.css('#subAgenda::text').get(),
        'total_value': response.css('#valorTotal::text').get(),
        'research_type': response.css('#tipoPesquisa::text').get()
        }

    # def parse_new(self, response):
    #     yield scrapy.FormRequest(
    #     url = 'http://pesquisasaude.saude.gov.br/pesquisas.xhtml',
    #     formdata = {
    #         'form':'form',
    #         'javax.faces.ViewState': view_state,
    #         'javax.faces.source':pagination,
    #         'javax.faces.partial.event':'click',
    #         'javax.faces.partial.execute':pagination + ' form',
    #         'javax.faces.partial.render':'form',
    #         'javax.faces.behavior.event':'action',
    #         'javax.faces.partial.ajax': 'true'
    #     },
    #     callback = self.parse_page,
    #     dont_filter = True
    # )


    

        

    
        
    