import scrapy
import json
import csv
import itertools

class AldiSpider(scrapy.Spider):
    name = "aldi"
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.aldi.com.au/', callback=self.parse)

    def parse(self, response):
        menuItems = response.xpath('//nav[@class="main-nav main-nav--level-container"]//a/@href').extract()
        groceries = []
        for item in menuItems:
            if "groceries" in item:
                groceries.append(item)
        filename = f'groceries.csv'
        with open(filename, 'w',newline='') as f:
            employee_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(['Product_title', 'Product_image', 'Packsize', 'Price', 'Price per unit'])
        self.log(f'Saved file {filename}')
        for i in groceries:
            yield scrapy.Request(url=i, callback=self.items)
        
    def items(self,response):
        if (response.css("div.tx-aldi-products")):

            products = response.css("div.tx-aldi-products")
            print(products)
            filename = f'groceries.csv'

            with open(filename, 'a', newline='') as f:
                employee_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for item in products:

                    name = item.css('div.box--description--header::text').getall()
                    image = item.css('img').xpath('@src').getall()
                    info = item.css('div.box--price')
                    info.getall()
                    for n,i in enumerate(info):
                        ProductTitle = name[n].strip()
                        ProductImage = image[n]
                        PackSize = i.xpath('span[@class="box--amount"]/text()').get(default='N/A')
                        PriceDollars = i.xpath('span[@class="box--value"]/text()').get(default='')
                        PriceCents = i.xpath('span[@class="box--decimal"]/text()').get(default='c')
                        Price = PriceDollars + PriceCents
                        PricePerUnit = i.xpath('span[@class="box--baseprice"]/text()').get(default='')
                        employee_writer.writerow([ProductTitle, ProductImage, PackSize, Price, PricePerUnit])

            self.log(f'Saved file {filename}')