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

# df_consolidated = pd.DataFrame(columns=['Security Code','Company Name','Type','Date Begin','Date End',
# 'Net Sales',
#  'Other Income',
#  'Total Income',
#  'Cost of Materials Consumed',
#  'Finance Costs',
#  'Other Expenses',
#  'Purchases of stock-in-trade',
#  'Changes in inventories of finished goods, work-in-progress and stock-in-trade',
#  'Employee benefit expense',
#  'Depreciation and amortisation expense',
#  'Profit after Interest but before Exceptional Items',
#  'Exceptional Item',
#  'Profit (+)/ Loss (-) from Ordinary Activities before Tax',
#  'Tax',
#  'Current tax',
#  'Deferred tax',
#  'Net Profit (+)/ Loss (-) from Ordinary Activities after Tax',
#  'Net movement in regulatory deferral account balances',
#  'Net Profit Loss for the period from continuing operations',
#  'Profit (loss) from discontinuing operations before tax',
#  'Tax expense of discontinuing operations',
#  'Net profit (loss) from discontinuing operation after tax',
#  'Share of profit(loss) of associates and joint ventures',
#  'Net Profit',
#  'Minority Interest',
#  'Share of Profit & Loss of Asso',
#  'Net Profit after Mino Inter & Share of P & L',
#  'Any Other',
#  'Income Attributable to Consolidated Group',
#  'Other Comprehensive Income Net of Taxes',
#  'Total Amount of items that will not be reclassified to profit and loss',
#  'Income tax relating to items that will not be reclassified to profit or loss',
#  'Total Amount of items that will be reclassified to profit and loss',
#  'Income tax relating to items that will be reclassified to profit or loss',
#  'Any Other Comprehensive Item',
#  'Total Comprehensive Income for the Period',
#  'Basic EPS for continuing operation',
#  'Diluted EPS for continuing operation',
#  'Basic for discontinued & continuing operation',
#  'Diluted for discontinued & continuing operation'])

# df_standalone = pd.DataFrame(columns=['Security Code','Company Name','Type','Date Begin','Date End',
# 'Net Sales/Revenue From Operations',
#  'Other Income',
#  'Total Income',
#  'Cost of Materials Consumed',
#  'Finance Costs',
#  'Other Expenses',
#  'Changes in inventories of finished goods, work-in-progress and stock-in-trade',
#  'Depreciation and amortisation expense',
#  'Employee benefit expense',
#  'Purchases of stock-in-trade',
#  'Profit after Interest but before Exceptional Items',
#  'Profit (+)/ Loss (-) from Ordinary Activities before Tax',
#  'Current tax',
#  'Deferred tax',
#  'Net Profit (+)/ Loss (-) from Ordinary Activities after Tax',
#  'Net Profit',
#  'Basic EPS for continuing operation',
#  'Diluted EPS for continuing operation',
#  'Basic for discontinued & continuing operation',
#  'Diluted for discontinued & continuing operation'])

# rows = []
# # with open("quarterly_yearly_results.csv", 'r') as file:
# #     csvreader = csv.reader(file)
# #     # header = next(csvreader)
# #     for row in csvreader:
# #         rows.append(row)
# # # print(header)
# print(len(rows))
# links = []
# for row in rows:
#     for link in row:
#         links.append(row)

# print(links[:1])
# print(len(links))
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
        

