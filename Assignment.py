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

reports = []
for url in links:
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    reports.append(soup.get_text())

#print(f'Total {len(reports)} reports found')

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