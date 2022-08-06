# %%
import pandas as pd
import requests
import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
import nltk
import os, os.path
from collections import Counter

# %%
nltk.download('punkt')
nltk.download("stopwords")

# %%
excel_data_df =  pd.read_excel('Input.xlsx')
excel_data_df.head()
links = excel_data_df['URL']
URlID = excel_data_df['URL_ID']
print(f'Total {len(links)} reports found')
print(f'Total {len(URlID)} reports found')

# %%
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
            f = open(f'Textfiles/{URlID[i]}.txt', 'w+', encoding='utf-8')
            f.write(''+s.extract().text)
            f.close() 
        for data in soup.find_all("p"):
            f = open(f'Textfiles/{URlID[i]}.txt', 'a', encoding='utf-8')
            f.write('\n'+ data.get_text())
            f.close() 
        i=i+1 


# %%
with open('StopWords/StopWords_Generic.txt','r') as f:
    stop_words_generic = f.read()

stop_words_generic = stop_words_generic.split('\n')
print(f'Total number of Stop Words are {len(stop_words_generic)}')

# %%
with open('MasterDictionary/positive-words.txt','r') as f:
    positive_words = f.read()

positive_words = positive_words.split('\n')
print(f'Total number of Positive Words are {len(positive_words)}')

# %%
with open('MasterDictionary/negative-words.txt','r') as f:
    negative_words = f.read()

negative_words = negative_words.split('\n')
print(f'Total number of Negative Words are {len(negative_words)}')

# %%
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
    
def countfunc(positive, negative, words):
    score = 0
    
    paragraph = " ".join(words)
    count = Counter(paragraph.split())
    pos = 0
    neg = 0
    for key, val in count.items():
        key = key.rstrip('.,?!\n') # removing possible punctuation signs
        if key in positive:
            pos += val
        if key in negative:
            neg += val

    return pos, neg

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

def count_syllables(word):
    for i in range(len(word)):
        return len(
            re.findall('(?!e$)[aeiouy]+', word[i], re.I) +
            re.findall('^[^aeiouy]*e$', word[i], re.I)
    )
    
def find_personal_pronouns(word):
    text = ' '.join(word)

    for i in range(len(text)):
        pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
        pronouns = pronounRegex.findall(text)
        return len(pronouns)

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
    

# %%
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

# %%
total_words = 0
total_sentence_length = 0
for i in range(1,len(URlID)):
    with open(f'Textfiles/{i}.txt', 'r', encoding='utf8') as f:
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
                
                positive_score,negative_score = countfunc(positive_words, negative_words, words)
                 
                #print(f'Total positive score is {positive_score}')
                #print(f'Total negative score is {negative_score}')
                
                polarity_score = polarity(positive_score, negative_score)
                #print(polarity_score)
                
                subjectivity_score = subjectivity(positive_score, negative_score, num_words)
                #print(subjectivity_score)
                #print(sentiment(polarity_score))
                
                sentences = sent_tokenize(content)
                num_sentences = len(sentences)
                
                total_words =   num_words + total_words
                total_sentence_length = total_sentence_length + num_sentences
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
                
                sen = words
                average_word_length = sum(len(sens) for sens in sen)/ len(sen)
                
                syllable_count = count_syllables(words)
                
                personal_pronouns = find_personal_pronouns(words)
                
                
                excel_data_df.loc[i,'positive_score'] = positive_score
                excel_data_df.loc[i,'negative_score'] = negative_score
                excel_data_df.loc[i,'polarity_score'] = polarity_score
                excel_data_df.loc[i,'subjectivity_score'] = subjectivity_score
                excel_data_df.loc[i,'average_sentence_length'] = average_sentence_length
                excel_data_df.loc[i,'percentage_of_complex_words'] = percentage_complexwords
                excel_data_df.loc[i,'fog_index'] = fog_index
                excel_data_df.loc[i,'avg_number_of_words_per_sentence'] = total_words/total_sentence_length
                excel_data_df.loc[i,'complex_word_count'] = num_complexword
                excel_data_df.loc[i,'word_count'] = num_words
                excel_data_df.loc[i,'syllable_count'] = syllable_count
                excel_data_df.loc[i,'personal_pronouns'] = personal_pronouns
                excel_data_df.loc[i,'avg_word_length'] = average_word_length
                
                

# %%
excel_data_df.head()


# %%
options = {}
options['strings_to_formulas'] = False
options['strings_to_urls'] = False
new_path = r"G:\Projects\Python\Data-Extraction\Output Data Structure.xlsx"
writer = pd.ExcelWriter(new_path, engine='xlsxwriter',options=options)
excel_data_df.to_excel(writer)
writer.save()


