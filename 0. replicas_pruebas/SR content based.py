#!/usr/bin/env python
# coding: utf-8

# In[1]:


# source https://github.com/BindhuVinodh/Contentbased-recommendation
#https://medium.com/@bindhubalu/content-based-recommender-system-4db1b3de03e7
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel 
ds = pd.read_csv("sample-data.csv")


# In[7]:


ds.head(15)


# In[3]:


tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['description'])

print('OBTENCION DE CARACTERISTICAS')
print(tf.get_feature_names())
print(tfidf_matrix.shape)
# In[4]:


cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) 
results = {}
for idx, row in ds.iterrows():
   similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
   similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices] 
   results[row['id']] = similar_items[1:]


# In[5]:


def item(id):
    return ds.loc[ds['id'] == id]['description'].tolist()[0].split(' - ')[0]


# In[6]:


# Just reads the results out of the dictionary.
def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")
    print("-------")
    recs = results[item_id][:num]
    for rec in recs:
        print("Recommended: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")

recommend(item_id=11, num=5)


# In[ ]:




