import scrapy
import ast
import csv

class BseCrawlerSpider(scrapy.Spider):
    name = 'bse_crawler'
    allowed_domains = ['bseindia.com']
    start_urls = ['https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w?Group=&Scripcode=&industry=&segment=Equity&status=Active']

    def parse(self, response):
        scripts =  response.text
        list_of_dicts = ast.literal_eval(scripts)
        print(len(list_of_dicts))
        list_of_codes = []
        for dict_script in list_of_dicts:
            list_of_codes.append(dict_script['SCRIP_CD'])
        print(len(list_of_codes))
        # print(list_of_codes)
        urls = []
        for code in list_of_codes:
            urls.append('https://www.bseindia.com/corporates/Comp_Results.aspx?Code=' + code)
        # print(urls)
        # print(len(urls))
        for url in urls:
            yield response.follow(url, self.parse_script)
    
    def parse_script(self,response):
        links =  response.xpath('//*[@class="tablebluelink"]/@href').extract()[1:]
        for i in range(len(links)):
            links[i] = 'https://www.bseindia.com/corporates/' + links[i]
        urls = []
        for i in range(len(links)):
            if links[i].find('.pdf') == -1 and links[i].find('.PDF') == -1 :
                urls.append(links[i])   

        with open('quarterly_yearly_results.csv', 'a', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            if(len(urls)!=0):
                wr.writerow(urls)
            else:
               print(response.url)
               print('check website')
       




