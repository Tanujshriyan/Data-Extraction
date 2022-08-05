import pandas as pd
import requests
import re
from nltk import word_tokenize
from nltk import sent_tokenize
from bs4 import BeautifulSoup


excel_data_df =  pd.read_excel('Input.xlsx')
links = excel_data_df['URL']
URlID = excel_data_df['URL_ID']

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

i = 0
for url in links:
        r = requests.get(url, headers=headers)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        #print(soup)
        for each in ['header','title','p']:
            s = soup.find(each)
            #print(p)
            f = open(f'{URlID[i]}.txt', 'w+')
            f.write(s.extract().text)
            f.close() 
        i=i+1 
        