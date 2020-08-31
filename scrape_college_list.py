#!/usr/bin/env python
# coding: utf-8

# In[4]:


import bs4
from bs4 import BeautifulSoup
import requests
import re
import nltk
nltk.download()


# In[6]:


stop_words = set(nltk.corpus.stopwords.words('english'))


# In[17]:


def getAbbreviation(s) :
    abb = ''
    for word in s.split():
#         print(word)
        if word.lower() not in stop_words :
            abb += word[0].upper()
    return abb


# In[20]:


r = requests.get('https://www.4icu.org/in/a-z/')


# In[21]:


bs = BeautifulSoup(r.content,features='lxml')


# In[22]:


pattern = re.compile(r'/reviews/(\d+).htm')


# In[23]:


college_list = bs.findAll('a',{'href' : pattern})


# In[24]:


len(college_list)


# In[25]:


college_list[0].get_text()


# In[26]:


SITE = " https://cgpa-book.herokuapp.com/academia/college"
import time


# In[21]:


for college in college_list[756:] :
    i = 1 
    query = {
        'college' : college.get_text(),
        'abbreviation' : getAbbreviation(college.get_text())
    }
    r = requests.post(SITE,json=query)
    if r.status_code != 200 :
        print(i,r.status_code)
    i+=1
#     time.sleep(2)


# In[ ]:




