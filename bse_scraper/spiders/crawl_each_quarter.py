import scrapy
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


rows = []
with open(r"C:\Users\karti\Desktop\projects\bse_scraper\quarterly_yearly_results.csv", 'r') as file:
    csvreader = csv.reader(file)
    # header = next(csvreader)
    for row in csvreader:
        rows.append(row)
# print(header)
print(len(rows))
links = []
for row in rows:
    for link in row:
        links.append(link)

print(links[:50])
print(len(links))
urls = []
for i in range(len(links)):
    if links[i].find('.pdf') == -1 and links[i].find('.PDF') == -1 :
        urls.append(links[i])
print(urls[:50])
print(len(urls))
# j=0
class CrawlEachQuarterSpider(scrapy.Spider):
    name = 'crawl_each_quarter'
    allowed_domains = ['bseindia.com']
    start_urls = urls
    j=0
    df1 = pd.DataFrame()
    # def __init__(self):
    #     self.driver = webdriver.Chrome(ChromeDriverManager().install())


    def parse(self, response):
        dictA = {} 
        data =  response.xpath('//tr//tr//td/text()').extract()
        dictA['Company Name'] = response.xpath('//*[@id="ContentPlaceHolder1_lblcompname"]/text()').extract_first()
        dictA['Code'] = response.xpath('//*[@id="ContentPlaceHolder1_lblsrcipcode"]/text()').extract_first()
        dictA['Result Type'] = response.xpath('//*[@id="ContentPlaceHolder1_lblresulttype"]/text()').extract_first()
        for i in range(0,len(data),2):
            try:
                dictA[data[i]] = data[i+1]
            except:
                dictA[data[i]] = ""
        
        df2 = pd.DataFrame(dictA,index=[self.j])
#         print(df2.head())
        if(self.j==0):
            self.df1 = pd.DataFrame(dictA,index=[self.j])
#             print(df1.head())
        else:
            self.df1 = self.df1.merge(df2,how='outer')
#         print(df1)
        self.j= self.j +1
        print(self.j)
        if(self.j%1000 ==0):
            print(self.df1)
            self.df1.to_pickle('bse_data_scrapy.pkl')
        

