import pandas as pd
import requests
import re
from nltk import word_tokenize
from nltk import sent_tokenize
from bs4 import BeautifulSoup


excel_data_df =  pd.read_excel('Input.xlsx')
links = excel_data_df['URL']
URlID = excel_data_df['URLID']
#print(links)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

i = 0
for url in links:
        r = requests.get(url, headers=headers)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        #print(soup)
        for each in ['h1']:
            s = soup.find(each)
            #print(p)
            f = open(f'{URlID[i]}.txt', 'w+')
            f.write('Title: '+s.extract().text)
            f.close() 
        for data in soup.find_all("p"):
            f = open(f'{URlID[i]}.txt', 'a')
            f.write('\n'+ data.get_text())
            f.close() 
        i=i+1 

with open('StopWords/StopWords_Generic.text','r') as f:
    stop_words = f.read()

stop_words = stop_words.split('\n')
#print(f'Total number of Stop Words are {len(stop_words)}')

with open('MasterDictionary/positive-words.txt','r') as f:
    positive_words = f.read()

positive_words = positive_words.split('\n')
#print(f'Total number of Positive Words are {len(positive_words)}')

with open('MasterDictionary/negative-words.txt','r') as f:
    negative_words = f.read()

negative_words = negative_words.split('\n')
#print(f'Total number of Negative Words are {len(negative_words)}')