import scrapy


class QuotesSpider(scrapy.Spider):

    name = 'commodity'
    start_urls = [
        'http://www.joburgmarket.co.za/dailyprices.php'
    ]
    

    def parse(self, response):

        DATE = response.xpath('//div[@id="right2"]').css('p b ::text').extract_first()

        for index, item in enumerate(response.xpath('//tbody/tr')):

            if index:
                yield  {
                    index: item.css('td ::text').extract()
                }
            else:
                yield  {
                    'date': DATE, 
                    index: item.css('td ::text').extract()
                }
                
          