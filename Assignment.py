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

def tokenize(text):
    text = re.sub(r'[^A-Za-z]','',text.upper())
    tokenized_words = word_tokenize(text)
    return tokenized_words

def tokenize(text):
    text = re.sub(r'[^A-Za-z]',' ',text.upper())
    tokenized_words = word_tokenize(text)
    return tokenized_words

def remove_stopwords(words, stop_words):
    return [x for x in words if x not in stop_words]
    
def countfunc(store, words):
    score = 0
    for x in words:
        if(x in store):
            score = score+1
    return score

def sentiment(score):
    if(score < -0.5):
        return 'Most Negative'
    elif(score >= -0.5 and score < 0):
        return 'Negative'
    elif(score == 0):
        return 'Neutral'
    elif(score > 0 and score < 0.5):
        return 'Positive'
    else:
        return 'Very Positive'
    

def polarity(positive_score, negative_score):
    return (positive_score - negative_score)/((positive_score + negative_score)+ 0.000001)
     

def subjectivity(positive_score, negative_score, num_words):
    return (positive_score+negative_score)/(num_words+ 0.000001)

def syllable_morethan2(word):
    if(len(word) > 2 and (word[-2:] == 'es' or word[-2:] == 'ed')):
        return False
    
    count =0
    vowels = ['a','e','i','o','u']
    for i in word:
        if(i.lower() in vowels):
            count = count +1
        
    if(count > 2):
        return True
    else:
        return False
    
def fog_index_cal(average_sentence_length, percentage_complexwords):
    return 0.4*(average_sentence_length + percentage_complexwords)
    
var = ['positive_score',
      'negative_score',
      'polarity_score',
      'subjectivity_score',
      'average_sentence_length',
      'percentage_of_complex_words',
      'fog_index',
      'avg_number_of_words_per_sentence',
      'complex_word_count',
      'word_count',
      'syllable_count',
      'personal_pronouns',
      'avg_word_length']

for v in var:
    excel_data_df[v] = 0
    
excel_data_df.head()

for i in range(1,len(URlID)):
    with open(f'{i}.txt', 'r') as f:
        x = f.read()
        
        if x:
            start, end = 0, len(x)
            content = x[start:end] 
            if ('...' not in content) and ('. . .' not in content) and len(content) > 200:
                tokenized_words = tokenize(content) 
                #print(f'Total tokenized words are {len(tokenized_words)}')
                
                words = remove_stopwords(tokenized_words, stop_words_generic)
                num_words = len(words)
                #print(f'Total words after removing stop words are {len(words)}')
                
                positive_score = countfunc(positive_words,words)
                negative_score = countfunc(negative_words, words)
                #print(f'Total positive score is {positive_score}')
                #print(f'Total negative score is {negative_score}')
                
                polarity_score = polarity(positive_score, negative_score)
                #print(polarity_score)
                
                subjectivity_score = subjectivity(positive_score, negative_score, num_words)
                #print(subjectivity_score)
                #print(sentiment(polarity_score))
                
                sentences = sent_tokenize(content)
                num_sentences = len(sentences)
                average_sentence_length = num_words/num_sentences   
        
                num_complexword = 0
                
                for word in words:
                    if(syllable_morethan2(word)):
                        num_complexword = num_complexword+1
                        
                #print(num_complexword)
                percentage_complexwords = num_complexword/num_words
                #print(percentage_complexwords)
                fog_index = fog_index_cal(average_sentence_length, percentage_complexwords)
                #print(fog_index)
                
                positive_word_proportion = positive_score/num_words
                negative_word_proportion = negative_score/num_words
                
                